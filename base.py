import torndb
import hashlib

The MIT License (MIT)

Copyright (c) 2015 Bostjan Jerko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

class accounts:
    # create a database in mysql (create database accounts)
    # create user and give it database access (CREATE USER 'accounts'@'localhost' IDENTIFIED BY 'stnuocca';)
    #(GRANT ALL PRIVILEGES ON accounts.* TO 'accounts'@'localhost';)

    def __init__(self):
        userName='accounts'
        databaseName='accounts'
        password='stnuocca'
        self.db=torndb.Connection("localhost", databaseName, userName, password, charset="utf8")
        self.db.execute("create table if not exists accounts( \
            username varchar(20) not null, \
            password varchar(32) not null, \
            is_admin boolean not null)")

    def create_user(self, name, password, is_admin):
        ret=self.db.execute("select count(*) from accounts where username=%s", name)
        if ret==0:
            self.db.execute("insert into accounts(username, password, is_admin) values (%s, %s, %s)", name, hashlib.md5(password).hexdigest(), is_admin)

    def delete_user(self, name):
        self.db.execute("delete from accounts where username=%s limit 1", name)

    def is_user(self, name, password):
        ret=self.db.get("select count(*) from accounts where username=\"%s\" and password=\"%s\"", name, password)
        if ret!=0:
            return True
        else:
            return False

    def close_db(self):
        self.db.close()


if __name__=="__main__":
    print "testing"
    a = accounts()
    a.create_user('bostjan', 'najtsob', True)
    a.close_db()
