import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import ProfileNotFound
import argparse

class NoInstanceFound(Exception):
    def __init__(self):
        Exception.__init__(self, \
                           "No Instances were found with the Tag/Value pair")

def list_instance_id(region, profile, tag, value, rebootInstance):
    """"""

    instance_list = []
    tag = 'tag:' + tag
    try:
        session = boto3.Session(region_name=region, profile_name=profile)
        client_ec2 = session.client('ec2')

        response = client_ec2.describe_instances(
            Filters=[{'Name': tag, 'Values': [value]}
                     ],
            MaxResults=100
        )
        for i in response['Reservations']:
            temp_dict = {}
            for key, value in i.items():
                if key == 'Instances':
                    temp_dict['PrivateIpAddress'] = value[0].get('PrivateIpAddress', '')
                    temp_dict['PublicDnsName'] = value[0].get('PublicDnsName', '')
                    temp_dict['InstanceId'] = value[0]['InstanceId']
                    temp_dict['State'] = value[0]['State']['Name']
            instance_list.append(temp_dict)
        if len(instance_list) !=0:
            check_instance_state(region, profile, instance_list, rebootInstance)
        else:
            raise NoInstanceFound

    # Catch Error while Calling the API
    except ClientError as e:
        print(str(e))
    # Catch Error while Paring the API response.
    except KeyError as e:
        print "KeyError: " + str(e)
    except ValueError as e:
        print str(e)
    # Ctach error when Boto3 is not able to find the AWS profile_name.
    except ProfileNotFound as e:
        print str(e)
    # Custom Exception : When no instances are returned with the API call.
    except NoInstanceFound as e:
        print str(e)

def check_instance_state(region, profile, instance_list, rebootInstance):
    instance_rebooted = []
    instance_not_rebooted = []
    for i in instance_list:
        if i['State'] == 'running':
            temp_list = [i['InstanceId'], i['PublicDnsName'], i['PrivateIpAddress']]
            instance_rebooted.append(temp_list)
        else:
            temp_list = [i['InstanceId'], i['State'], i['PublicDnsName'], i['PrivateIpAddress']]
            instance_not_rebooted.append(temp_list)



    if not rebootInstance:
        print "The Instance were Not restarted. Set --reboot Flag to True. Use Help Flag for more details."
        print
        print
    else:
        if len(instance_rebooted) == 0:
            print "No Instances to Reboot"
        else:
            print "The Instance were Restarted"
            print
            print
            restart_instance(region, profile, instance_rebooted)

    print "The Instance not in state to restart. Count : " + str(len(instance_not_rebooted))
    for i in instance_not_rebooted:
        print "Instance : " + i[0] + ", Instance State : " + i[1] +\
                        ", PublicDNSName : " + i[2] + ", Private IP : " + i[3]
    print


    print "The Instances up for Restart. Count : " + str(len(instance_rebooted))
    for i in instance_rebooted:
        print "Instance : " + i[0] + ", Instance State : Running, PublicDNSName : " + i[1] + ", Private IP : " + i[2]
    print




def restart_instance(region, profile, instance_rebooted):
    print "Restarting the Instance"
    session = boto3.Session(region_name=region, profile_name=profile)
    client_restart = session.client('ec2')
    temp_list = []
    for i in instance_rebooted:
        temp_list.append(i[0])

    instance_rebooted= temp_list

    client_restart.reboot_instances(
        InstanceIds=instance_rebooted
    )





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-reboot", "--reboot-instance", dest="rebootInstance", default=False,
                        help="List the instance to reboot or not. Set this to true or false")
    parser.add_argument("-tag", "--tag-name", dest="tag", default="", help="Describe the Tag Name")
    parser.add_argument("-value", "--tag-value", dest="value", default="", help="Describe the Value")
    parser.add_argument("-region", "--region-name", dest="region", default="us-west-2", help="Input the Region Name")
    parser.add_argument("-profile", "--profile-name", dest="profile", default="dev", help="Input the Profile Name")
    args = parser.parse_args()
    region = args.region
    profile = args.profile
    tag = args.tag
    value = args.value
    rebootInstance = args.rebootInstance


    if len(args.tag) == 0 or len(args.value) == 0:
        print "Tag and value are required."
    elif type(rebootInstance) != bool:
        print "Valid Input for reboot flag is True|False"
    else:
        list_instance_id(region, profile, tag, value,rebootInstance)