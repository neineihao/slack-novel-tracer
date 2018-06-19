import configparser

def parser(file="config.ini"):
    result_d = {}
    config = configparser.ConfigParser()
    config.read(file)
    result_d['OAuth'] = config['slack_ini']['OAuth']
    result_d['bot-OAuth'] = config['slack_ini']['Bot User OAuth']
    return result_d

if __name__ == '__main__':
    result = parser()
    print(result['access_token'])
    print(result['secret'])