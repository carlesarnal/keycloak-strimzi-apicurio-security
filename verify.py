"""Real Keycloak, Strimzi OAuth Kafka and Registry authorization boundaries."""
import json
from pathlib import Path
import subprocess
import time
import urllib.parse
import urllib.request
import urllib.error

ROOT=Path(__file__).resolve().parent


def compose(*args, data=None, check=True):
    result=subprocess.run(['docker','compose','-f',str(ROOT/'compose.yaml'),'-p','security-lab',*args],
                          input=data,text=True,capture_output=True,timeout=180)
    if check and result.returncode:
        raise RuntimeError(result.stdout+result.stderr)
    return result.stdout+result.stderr


def request(port,path,token=None,body=None,method='GET',expected=(200,201,204)):
    headers={}
    if token: headers['Authorization']='Bearer '+token
    if body is not None: headers['Content-Type']='application/json'
    req=urllib.request.Request(f'http://localhost:{port}'+path,data=None if body is None else json.dumps(body).encode(),headers=headers,method=method)
    try:
        with urllib.request.urlopen(req,timeout=15) as response: status,raw=response.status,response.read()
    except urllib.error.HTTPError as error: status,raw=error.code,error.read()
    assert status in expected,(path,status,raw.decode())
    return status,json.loads(raw) if raw else None


def token(client):
    data=urllib.parse.urlencode({'grant_type':'client_credentials','client_id':client,'client_secret':'local-lab-'+client}).encode()
    with urllib.request.urlopen(urllib.request.Request('http://localhost:18230/realms/lab/protocol/openid-connect/token',data=data),timeout=10) as response:
        return json.load(response)['access_token']


def kafka(tool,*args,data=None,check=True):
    return compose('exec','-T','kafka','/opt/kafka/bin/'+tool,*args,data=data,check=check)


def run():
    try:
        compose('up','-d','keycloak')
        for attempt in range(90):
            try: admin=token('publisher'); reader=token('reader'); break
            except OSError:
                if attempt==89: raise
                time.sleep(2)
        compose('up','-d','registry','kafka')
        for attempt in range(90):
            try: request(18231,'/apis/registry/v3/groups',admin); break
            except (OSError,AssertionError):
                if attempt==89: raise
                time.sleep(2)
        request(18231,'/apis/registry/v3/groups','invalid-token',expected=(401,))
        request(18231,'/apis/registry/v3/groups',admin,{'groupId':'lab'},'POST')
        path='/apis/registry/v3/groups/lab/artifacts'
        body={'artifactId':'contract','artifactType':'JSON','firstVersion':{'version':'1','content':{'content':'{"type":"string"}','contentType':'application/json'}}}
        request(18231,path,admin,body,'POST')
        _,before=request(18231,path+'/contract/versions/1/content',reader)
        denied,_=request(18231,path+'/contract/versions',reader,{'version':'2','content':{'content':'{"type":"number"}','contentType':'application/json'}},'POST',expected=(403,))
        _,after=request(18231,path+'/contract/versions/1/content',reader)
        assert before==after
        request(18231,path+'/contract/versions/2',admin,expected=(404,))
        for attempt in range(60):
            try:
                kafka('kafka-topics.sh','--bootstrap-server','kafka:9092','--create','--if-not-exists','--topic','orders','--partitions','1','--replication-factor','1')
                break
            except RuntimeError:
                if attempt==59: raise
                time.sleep(2)
        kafka('kafka-acls.sh','--bootstrap-server','kafka:9092','--add','--allow-principal','User:service-account-publisher','--operation','Write','--operation','Describe','--topic','orders')
        def produce(client):
            return kafka('kafka-console-producer.sh','--bootstrap-server','kafka:9094','--topic','orders',
                         '--producer.config',f'/opt/lab/clients/{client}.properties',
                         '--producer-property','delivery.timeout.ms=10000','--producer-property','request.timeout.ms=5000',
                         '--producer-property','enable.idempotence=false',data=client+'\n',check=False)
        allowed=produce('publisher')
        assert 'Exception' not in allowed, allowed
        denied_kafka=produce('reader')
        assert 'TopicAuthorizationException' in denied_kafka,denied_kafka
        content=kafka('kafka-console-consumer.sh','--bootstrap-server','kafka:9092','--topic','orders','--partition','0','--offset','earliest','--timeout-ms','5000',check=False)
        records=[line.strip() for line in content.splitlines() if line.strip() in ('publisher','reader')]
        assert records==['publisher'],content
        report={'invalid_token_http':401,'readonly_lookup':'passed','readonly_mutation_http':denied,
                'accepted_content_unchanged':True,'rejected_version_absent':True,
                'kafka_publisher':'record observed','kafka_reader':'TopicAuthorizationException; record absent',
                'boundary':'real OAuth/ACL integration in Compose; internal admin listener and plaintext are lab-only; Kubernetes/TLS not established'}
        (ROOT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
    except Exception:
        logs=compose('logs','kafka',check=False)
        print('\n'.join(line for line in logs.splitlines() if any(word in line for word in ('ERROR','Exception','Caused by'))))
        raise
    finally: compose('down','-v',check=False)


if __name__=='__main__': run()
