import time
import boto3
from boto3.dynamodb.conditions import Key

def Actulizar_Json():
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table('Stargo_API')

#////////////////////////////Get Datos \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  response = table.query(KeyConditionExpression=Key('Timestamp').eq("ultimo"))
  name = response['Items'][0]['Nombre']
  ipPublica = response['Items'][0]['Ip_Publica']
  mac = response['Items'][0]['Mac_Address']
  estado_raw = response['Items'][0]['Estado']
  if int(estado_raw) == 1:
    estado = "Activo"
  else:
    estado="inactivo"
  B_Recv_0 = response['Items'][0]['Bytes_Recibidos']
  B_Sent_0 = response['Items'][0]['Bytes_Enviados']
  response = table.query(KeyConditionExpression=Key('Timestamp').eq("anterior"))
  B_Recv_m1 = response['Items'][0]['Bytes_Recibidos']
  B_Sent_m1 = response['Items'][0]['Bytes_Enviados']
#////////////////////////////Calcular Valores \\\\\\\\\\\\\\\\\\\\\\\\\\
  volumen_Recv = int(B_Recv_0)-int(B_Recv_m1)
  volumen_Sent = int(B_Sent_0)-int(B_Sent_m1)
  kbps_Recv = ((int(B_Recv_0)-int(B_Recv_m1))*8)/(300*1024)
  kbps_Sent = ((int(B_Sent_0)-int(B_Sent_m1))*8)/(300*1024)
#///////////////////////////Actualizar Json\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  response = table.put_item(Item={'Timestamp': "json",'Nombre': name,'Ip_Publica': ipPublica,\
      'Mac_Address': mac[3:5]+":"+mac[5:7]+":"+mac[7:9]+":"+mac[9:11]+":"+mac[11:13]+":"+mac[13:15],
      'Estado': estado, 'Bytes_Recibidos': str(volumen_Recv),'Bytes_Enviados': str(volumen_Sent), \
      'Kbps_Recibidos':  str(kbps_Recv),   'Kbps_Enviados': str(kbps_Sent)})
  print(volumen_Recv)
  print(volumen_Sent)
