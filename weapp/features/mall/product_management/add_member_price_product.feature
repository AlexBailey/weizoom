# __author__ : "��ѩ��"
Feature: ����л�Ա�ۿ۵���Ʒ
	Jobs��ͨ������ϵͳ���̳��������"��Ա�ۿ۵���Ʒ"


Background:
	Given jobs��¼ϵͳ
	And jobs�������Ʒ���
		"""
		[{
			"name": "�ߴ�",
			"type": "����",
			"values": [{
				"name": "M"
			}, {
				"name": "S"
			}]
		}]
		"""
	When jobs��ӻ�Ա�ȼ�
		"""
		[{
			"name": "ͭ�ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "9"
		}, {
			"name": "���ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "8"
		}, {
			"name": "���ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "7"
		}]
		"""
	Then jobs�ܻ�ȡ��Ա�ȼ��б�
		"""
		[{
			"name": "��ͨ��Ա",
			"upgrade": "�Զ�����",
			"discount": "10"
		}, {
			"name": "ͭ�ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "9"
		}, {
			"name": "���ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "8"
		}, {
			"name": "���ƻ�Ա",
			"upgrade": "�ֶ�����",
			"discount": "7"
		}]
		"""
	When jobs�����֧����ʽ
		"""
		[{
			"type": "��������",
			"description": "�ҵĻ�������",
			"is_active": "����"
		},{
			"type": "΢��֧��",
			"description": "�ҵ�΢��֧��",
			"is_active": "����",
			"weixin_appid": "12345",
			"weixin_partner_id": "22345",
			"weixin_partner_key": "32345",
			"weixin_sign": "42345"
		}]
		"""

@mall2
Scenario: ����л�Ա�ۿ۵���Ʒ
	jobs��ӻ�Ա�ۿ۵���Ʒ���ܻ�ȡ����ӵ���Ʒ

	#��ӵ���Ʒʹ���˻�Ա�ȼ��ۿ�
	Given jobs��¼ϵͳ
	When jobs�������Ʒ
		"""
		[{
			"name": "��Ʒ1",
			"price": 100.00,
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "����",
						"stocks": 2
					}
				}
			}
		}, {
			"name": "��Ʒ2",
			"is_member_product": "on",
			"is_enable_model": "���ù��",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "����"
					},
					"S": {
						"price": 300,
						"stock_type": "����"
					}
				}
			}
		}]
		"""
	Then jobs�ܻ�ȡ��Ʒ'��Ʒ1'
		"""
		{
			"name": "��Ʒ1",
			"is_member_product": "on",
			"model": {
				"models": {
					"standard": {
						"price": 100.00,
						"stock_type": "����",
						"stocks": 2
					}
				}
			}
		}
		"""
		#	"price": 100.00,
	Then jobs�ܻ�ȡ��Ʒ'��Ʒ2'
		"""
		{
			"name": "��Ʒ2",
			"is_member_product": "on",
			"is_enable_model": "���ù��",
			"model": {
				"models":{
					"M": {
						"price": 300,
						"stock_type": "����"
					},
					"S": {
						"price": 300,
						"stock_type": "����"
					}
				}
			}
		}
		"""