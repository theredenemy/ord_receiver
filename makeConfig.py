
import configparser


def makeConfig():
  import configparser
  config_file = configparser.ConfigParser()


  config_file.add_section("sftp")


  config_file.set("sftp", "host", "127.0.0.1")
  config_file.set("sftp", "port", "21")
  config_file.set("sftp", "user", "fsky")
  config_file.set("sftp", "key", "C:\\Users\\FSKY\\.ssh\\kulcs")

  config_file.add_section("ORD_SERVER")

  config_file.set("ORD_SERVER", "ip", "10.0.0.100")
  config_file.set("ORD_SERVER", "port", "5000")


  with open(r"receiver.ini", 'w') as configfileObj:
     config_file.write(configfileObj)
     configfileObj.flush()
     configfileObj.close()

  print("Config file 'receiver.ini' created")

if __name__ == "__main__":
   makeConfig()