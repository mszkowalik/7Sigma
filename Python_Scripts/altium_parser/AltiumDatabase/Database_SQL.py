import mysql.connector
from mysql.connector import errorcode
import logging as log

class Part:
    def __init__(self, dictionary,TableName = None):
        self.dictionary = dictionary 
        
        self.TableName = TableName

        self.part_number = dictionary['Part Number']
        self.schlib = dictionary['Library Ref']
        self.pcblib = dictionary['Footprint Ref']
        self.datasheet = dictionary['HelpURL']
        try:
            self.supplier = dictionary['Supplier 1']
        except:
            self.supplier = ''

        try:
            self.supplier_part_number = dictionary['Supplier Part Number 1'] 
        except:
            self.supplier_part_number = ''

        self.help_url = dictionary['HelpURL']
        self.manufacturer = dictionary['Manufacturer']
        self.manufacturer_part_number = dictionary['Manufacturer Part Number']

class AltiumDatabase:
    def __init__(self):
        verbose = False

        if verbose:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        else:
            log.basicConfig(format="%(levelname)s: %(message)s")

        # Obtain connection string information from the portal
        config = {
        'host':'altiumlib.mysql.database.azure.com',
        'user':'Altium@altiumlib',
        'password':'Altium123',
        'database':'Library'
        # ,
        # 'ssl_ca':'BaltimoreCyberTrustRoot.crt.pem'
        }

        # Construct connection string
        try:        
            self.connection = mysql.connector.connect(**config)
            log.info("Connection established")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.error("Something is wrong with the user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log.error("Database does not exist")
            else:
                log.error(err)
        else:
            cursor = self.connection.cursor()

        self.database = list()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        log.info("Fetched {} Tables".format(len(tables)))
        
        for table in tables:
            name = table[0]
            cursor.execute("SELECT * FROM `" + name + "`;")
            rows = cursor.fetchall()

            num_fields = len(cursor.description)
            field_names = [i[0] for i in cursor.description]

            before = len(self.database)

            for i in rows:
                self.database.append(Part(dict(zip(field_names,i)),name))

            after = len(self.database)
            log.info("{}: {} Components".format(name,after-before))
        cursor.close()

    def __del__(self):
            self.connection.commit()
            # self.cursor.close()
            self.connection.close()

    # def getAllFootprints(self):
    #     footprints = list()
    #     for part in self.componentsList:
    #         footprints.append(part.pcblib)
    #     footprints= list(dict.fromkeys(footprints))
    #     print(footprints)

    # def Statistics(self):
    #     allComponents = len(self.componentsList)
    #     allFootprints = self.getAllFootprints()
    #     return allFootprints
         



# if __name__ == "__main__":
#     conn = AltiumDatabase()
#     stats = conn.Statistics()


