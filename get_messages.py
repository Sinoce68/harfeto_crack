from bs4 import BeautifulSoup
from requests import post
from sys import *
from os import path

class GetMsg():
    
    def __init__(self, html:str, filename:str) -> None:
        self.html_code = html
        self.bs4 = BeautifulSoup(self.html_code, "html.parser")
        self.filename = filename
        self.fp = None

    def get_tr_tags(self):
        return self.bs4.find_all("tr")

    def get_td_tags(self):
        td_tags = []
        for tr_tag in self.get_tr_tags():
            td_tags.append(tr_tag.td)
        return td_tags
    
    def get_text_from_td_tags(self):
        messages = []
        for td_tag in self.get_td_tags():
            messages.append(td_tag.getText().replace("دانلود استوری پیام","").strip())
        return messages

    def get_text(self):
        return self.get_text_from_td_tags()
    
    def write_text(self):
        EXIST = None
        if path.isfile(self.filename):
            EXIST = True
        else:
            EXIST = False
        while EXIST:
            overwrite = int(input("OverWrite File Exist [1 => Y/ 2 => N]:> "))
            if overwrite == 1:
                open(self.filename,"w").write("")
                break
            else:
                print("Exiting ...")
        for x,message in enumerate(self.get_text()):
            open(self.filename, 'ab').write(f"""NUM:{x+1}        MSG:{message}\n""".encode("UTF-8"))

def main():
    url = input("Enter Url:> ")
    password = input("Enter Password:> ")
    result = post(url, data={"password":password, "submit":"نمایش  پیام های دریافتی"})
    if result.status_code == 200:
        print("STATUS:200")
        messsages = GetMsg(result.text,'msg.txt')
        for x,msg in enumerate(messsages.get_text()):
            print(F"{x+1}-{msg}")
        messsages.write_text()
    else:
        print(f"STATUS:{result.status_code}")


if __name__ == "__main__":
    main()