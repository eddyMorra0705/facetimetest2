#mobileconfig.py
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.dom.minidom

# 创建根元素
root = Element('plist', version='1.0')

# 创建dict元素
_dict = SubElement(root, 'dict')

# 添加Payload基础信息
SubElement(_dict, 'key').text = 'PayloadDisplayName'
SubElement(_dict, 'string').text = '🇺🇲 美国 03'

SubElement(_dict, 'key').text = 'PayloadIdentifier'
SubElement(_dict, 'string').text = 'com.example.vpn'

SubElement(_dict, 'key').text = 'PayloadType'
SubElement(_dict, 'string').text = 'Configuration'

SubElement(_dict, 'key').text = 'PayloadUUID'
SubElement(_dict, 'string').text = 'some-uuid-here'

SubElement(_dict, 'key').text = 'PayloadVersion'
SubElement(_dict, 'integer').text = '1'

# 添加VPN配置信息
SubElement(_dict, 'key').text = 'VPNType'
SubElement(_dict, 'string').text = 'Trojan'

SubElement(_dict, 'key').text = 'ServerAddress'
SubElement(_dict, 'string').text = '2pwiyzakfjnmvikqu7la.wgetapi.com'

SubElement(_dict, 'key').text = 'ServerPort'
SubElement(_dict, 'integer').text = '4046'

SubElement(_dict, 'key').text = 'Password'
SubElement(_dict, 'string').text = 'da06745f-bc5b-3d1a-83e8-689d747deda1'

SubElement(_dict, 'key').text = 'SNI'
SubElement(_dict, 'string').text = '92zpkcdwze29gaqizktn.appletls.com'

SubElement(_dict, 'key').text = 'SkipCertVerify'
SubElement(_dict, 'true').text = ''

# 创建ElementTree对象并写入文件
tree = ElementTree(root)

# 格式化输出
xml_str = xml.dom.minidom.parseString(ElementTree.tostring(root)).toprettyxml(indent="   ")

# 保存到.mobileconfig文件
with open("trojan_vpn_config.mobileconfig", "w") as f:
    f.write(xml_str)
