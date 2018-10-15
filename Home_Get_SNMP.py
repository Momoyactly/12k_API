from pysnmp.hlapi import *
import time
import boto3
from boto3.dynamodb.conditions import Key
def Get_and_Update_with_SNMP():
  carga_exitosa = True
  valores =[]
  dynamodb = boto3.resource("dynamodb")
  table = dynamodb.Table('Stargo_API')
  while carga_exitosa:
      errorIndication, errorStatus, errorIndex, varBinds = next(
          getCmd(SnmpEngine(),
                 CommunityData('o/aUzp6a'),
                 UdpTransportTarget(('snmp.meraki.com', 16100)),
                 ContextData(),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.4.1.2.136.21.68.253.245.224')),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.4.1.7.136.21.68.253.245.224')),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.4.1.1.136.21.68.253.245.224')),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.4.1.3.136.21.68.253.245.224')),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.5.1.6.136.21.68.253.245.224.0')),
                 ObjectType(ObjectIdentity('SNMPv2-SMI', 'enterprises','29671.1.1.5.1.7.136.21.68.253.245.224.0')))
      )

      if errorIndication:
          print(errorIndication)
      elif errorStatus:
          print('%s at %s' % (errorStatus.prettyPrint(),
                              errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
      else:
          
          carga_exitosa = False
          for varBind in varBinds:
             # print(str(varBind).split("=")[1])
              valores.append(str(varBind).split("=")[1])
          print(valores)
  response = table.query(KeyConditionExpression=Key('Timestamp').eq("ultimo"))
  response = response['Items'][0]
  print(response)
  table.put_item(Item={'Timestamp': 'anterior','Nombre': response['Nombre'],'Ip_Publica':response['Ip_Publica'],\
                'Mac_Address': response['Mac_Address'],'Estado': response['Estado'],\
                'Bytes_Recibidos': response['Bytes_Recibidos'],'Bytes_Enviados': response['Bytes_Enviados'] })
   
  table.put_item(Item={'Timestamp': 'ultimo','Nombre': valores[0],'Ip_Publica':valores[1],'Mac_Address':valores[2],\
                       'Estado': valores[3],'Bytes_Recibidos':valores[4],'Bytes_Enviados':valores[5] })
      