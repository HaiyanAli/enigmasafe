from functions import *
import argparse
import sys


def intro():
    print("""
 _____      _                       _____        __     
|  ___|    (_)                     /  ___|      / _|    
| |__ _ __  _  __ _ _ __ ___   __ _\ `--.  __ _| |_ ___ 
|  __| '_ \| |/ _` | '_ ` _ \ / _` |`--. \/ _` |  _/ _ \\
| |__| | | | | (_| | | | | | | (_| /\__/ / (_| | ||  __/
\____/_| |_|_|\__, |_| |_| |_|\__,_\____/ \__,_|_| \___|
               __/ |                                    
              |___/                  By Haiyan Productions
                                     Version 1.0
          
""")


if __name__ == "__main__":
    parse = argparse.ArgumentParser()

    parse.add_argument('-G','--gui',action="store_true" ,help="For GUI (Graphical user interface) Mode")

    parse.add_argument('-f','--file',metavar='File_path',help="The file path which you want to Encrypt or Decrypt")
    parse.add_argument('-e','--encrypt',action="store_true",help="Encrypt the File")
    parse.add_argument('-d','--decrypt',action="store_true",help="Decrypt the File")

    parse.add_argument('-s','--showpwd',action="store_true",help="Show the passwords list  [Notice: They don't show Password]")

    parse.add_argument('-g','--getpwd',metavar='Password_id',help="Get Password to the clipBoard")
    parse.add_argument('-a','--addpwd',action="store_true",help="Add password")

    parse.add_argument('-p', '--givepwd', metavar="lucd", help="Generate a random password. Use 'l' for lowercase letters, 'u' for uppercase letters, 'd' for digits, and 'c' for special characters. [default: lucd]")

    parse.add_argument('--changepwd',action="store_true",help="change login Password")


    intro()
    arg = parse.parse_args()
    num_args = len(sys.argv) - 1
    generate_default_dataBase()

    if num_args != 0:
        key = login()
        if key != False:
            if arg.file and arg.encrypt:
                encrypt_file(arg.file, key)
            elif arg.file and arg.decrypt:
                decrypt_file(arg.file, key)
            elif arg.addpwd:
                add_password(key)
            elif arg.showpwd:
                show_passwords()
            elif arg.getpwd:
                get_password(key, arg.getpwd)
            elif arg.givepwd:
                password_generater(arg.givepwd)
            elif arg.changepwd:
                add_login_cred()
            else:
                parse.print_help()
    else:
        parse.print_help()






