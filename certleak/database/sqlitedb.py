import logging
import pathlib
import sqlite3
import time
from threading import Lock

from .abstractdb import AbstractDB


class SQLiteDB(AbstractDB):
    def __init__(self, dbpath="certleak"):
        super().__init__()
        self.lock = Lock()
        self.db_path = pathlib.Path(dbpath)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing SQLite - %s", dbpath)

        # Check if the folder path exists
        if not self.db_path.exists():
            # If not, create the path and the file
            if not self.db_path.parent.exists():
                self.db_path.parent.mkdir(parents=True)

            self.db_path.touch()
        elif self.db_path.is_dir():
            msg = f"'{self.db_path}' is a directory. Use different path/name for database."
            raise ValueError(msg)

        try:
            self.db = sqlite3.connect(str(self.db_path.absolute()), check_same_thread=False)
            self.db.text_factory = lambda x: str(x, "utf-8", "ignore")
            self.cursor = self.db.cursor()
            self._create_tables()
        except Exception:
            self.logger.exception("An exception occurred when initializing the database")
            raise

        self.logger.debug("Connected to database!")

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "certs" (
              "fingerprint" TEXT,
              "not_before"  INTEGER,
              "not_after" INTEGER,
              "serial_number" TEXT,
              "subjectC"  TEXT,
              "subjectCN" TEXT,
              "subjectL"  TEXT,
              "subjectO"  TEXT,
              "subjectOU" TEXT,
              "subjectST" TEXT,
              "subjectAggregated" TEXT,
              "extensionsAuthorityInfoAccess" TEXT,
              "extensionsAuthorityKeyIdentifier"  TEXT,
              "extensionsBasicConstraints"  TEXT,
              "extensionsCertificatePolicies" TEXT,
              "extensionsCtlSignedCertificateTimestamp" TEXT,
              "extensionsExtendedKeyUsage"  TEXT,
              "extensionsKeyUsage"  TEXT,
              "extensionsSubjectAltName"  TEXT,
              "extensionsSubjectKeyIdentifier"  TEXT,
              "all_domains" TEXT,
              "issuerAggregated"  TEXT,
              "stored_at" INTEGER,
              PRIMARY KEY("fingerprint")
            );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "domains" (
              "domain"  TEXT NOT NULL,
              "cert_fingerprint"  TEXT NOT NULL,
              "stored_at" INTEGER,
              PRIMARY KEY("domain","cert_fingerprint")
            );""")
        self.db.commit()

    def _insert_data(self, update):
        # self.cursor.execute("INSERT INTO ")
        cert = update.leaf_cert
        now = int(time.time())
        for domain in update.all_domains:
            self.cursor.execute("INSERT INTO domains (domain, cert_fingerprint, stored_at) VALUES (?, ?, ?)", (domain, cert.fingerprint, now))
            self.db.commit()
        self.cursor.execute(
            "INSERT INTO certs (fingerprint, not_before, not_after, serial_number, all_domains, subjectCN, stored_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (cert.fingerprint, cert.not_before, cert.not_after, cert.serial_number, ", ".join(cert.all_domains), cert.subject.CN, now),
        )
        self.db.commit()

    def store(self, update):
        self.logger.debug("Storing cert_update %s", update.cert_index)

        try:
            with self.lock:
                self._insert_data(update)
        except Exception as e:
            self.logger.debug("Exception '%s'", e)
