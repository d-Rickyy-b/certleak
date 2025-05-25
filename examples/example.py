import logging
from pathlib import Path

from certleak import CertLeak
from certleak.actions import DatabaseAction, LogAction
from certleak.analyzers import AuthorityKeyIDAnalyzer, DNStwistAnalyzer, FullDomainAnalyzer, LetsEncryptAnalyzer, TLDAnalyzer, WildcardCertAnalyzer, X509Analyzer
from certleak.database import SQLiteDB

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("certleak.util.threadingutils").setLevel(logging.ERROR)
logaction = LogAction(level=logging.INFO, template="${analyzer_name} found: ${leaf_cert.subject.CN} () - ${leaf_cert.all_domains}")

# Initialize CertLeak object
certleak = CertLeak(certstream_url="ws://127.0.0.1:8080/")
# certleak = CertLeak()

db_path = Path.cwd().resolve() / "phish.db"
db = SQLiteDB(str(db_path))
db_action = DatabaseAction(db)

xyz_analyzer = TLDAnalyzer(logaction, ["xyz"], blacklist="acmetestbykeychestdotnet") & X509Analyzer()
phishing_analyzer = FullDomainAnalyzer([db_action, logaction], ["idcheck", "logins"])
paypal_analyzer = FullDomainAnalyzer(db_action, ["paypal"])

analyzer6 = AuthorityKeyIDAnalyzer(logaction, "E6:A3:B4:5B:06:2D:50:9B:33:82:28:2D:19:6E:FE:97:D5:95:6C:CB")

w1 = WildcardCertAnalyzer([db_action, logaction]) & X509Analyzer()
l1 = LetsEncryptAnalyzer(db_action) & X509Analyzer()
# ata = AlwaysTrueAnalyzer(actions=db_action) & X509Analyzer()

dns3 = DNStwistAnalyzer(logaction, "paypal.com") & X509Analyzer()

certleak.add_analyzer(dns3)

certleak.add_analyzer(paypal_analyzer)
certleak.add_analyzer(phishing_analyzer)
# certleak.add_analyzer(xyz_analyzer)

certleak.start()
