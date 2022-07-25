[![certleak logo created by https://t.me/AboutTheDot](https://raw.githubusercontent.com/d-Rickyy-b/certleak/master/docs/certleak_logo.png)](https://github.com/d-Rickyy-b/certleak)

# certleak - Cert-Monitoring Python Framework
[![Run tests and lint](https://github.com/d-Rickyy-b/certleak/workflows/Run%20tests%20and%20lint/badge.svg)](https://github.com/d-Rickyy-b/certleak/actions?query=workflow%3A%22Run+tests+and+lint%22)
[![PyPI version](https://badge.fury.io/py/certleak.svg)](https://pypi.org/project/certleak/)
[![Coverage Status](https://coveralls.io/repos/github/d-Rickyy-b/certleak/badge.svg?branch=master)](https://coveralls.io/github/d-Rickyy-b/certleak?branch=master)

Certleak is a tool to monitor and analyze TLS certificates as they are issued.
It is heavily inspired by [Phishing Catcher](https://github.com/x0rz/phishing_catcher) by [x0rz](https://twitter.com/x0rz). 

It utilizes the [Certificate Transparency Network](https://www.certificate-transparency.org/what-is-ct), which is an ecosystem for publicly monitoring issuance of TLS certificates.

A regular use case of this tool is to find phishing domains before they are actively used in the wild.

Instead of querying the single transparency log servers individually, certleak uses [certstream](https://certstream.calidog.io/) for analyzing certificates in real time.
To do that, it uses about 2600-3000 kbit/s of bandwidth.
Since certleak uses certstream, it only enables you to analyze live data.
There is no way to use this tool to analyze certificates that have been issued in the past or while being offline.

## Extensibility
Creating new analyzers or actions is as easy as creating a new python file.
Certleak is built with extensibility in mind.
Check the [analyzer docs](https://github.com/d-Rickyy-b/certleak/tree/master/certleak/analyzers/README.md) as well as the [actions docs](https://github.com/d-Rickyy-b/certleak/tree/master/certleak/actions/README.md).  


## Installation
Simply use pip to install this tool.
```
pip install certleak
```

## Usage
After downloading and installing the package, you only need to create a small python script in which you import certleak and set up the analyzers and the belonging actions.
Below you'll find an example configuration. Keep in mind that it's fully up to you what analyzers you want to add and which actions you want to be executed.

In general the workflow is as follows: `New Certificate -> Analyzer matches -> Actions are executed`

```python
# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from certleak import CertLeak
from certleak.actions import LogAction, DatabaseAction
from certleak.analyzers import (FullDomainAnalyzer, TLDAnalyzer, WildcardCertAnalyzer, X509Analyzer, LetsEncryptAnalyzer,
                                RegexDomainAnalyzer, DNStwistAnalyzer)
from certleak.database import SQLiteDB

certleak = CertLeak()

# Set up database
path = Path.cwd().absolute() / "phish.db"
db = SQLiteDB(str(path))

# Set up actions
db_action = DatabaseAction(db)
logaction = LogAction(level=logging.INFO, template="${analyzer_name} found: ${leaf_cert.subject.CN} () - ${leaf_cert.all_domains}")

# Set up analyzers
xyz_tld_analyzer = TLDAnalyzer(logaction, ["xyz"], blacklist="acmetestbykeychestdotnet") & X509Analyzer()
phishing_analyzer = FullDomainAnalyzer([db_action, logaction], ["paypal", "amazon"])
regex_analyzer = RegexDomainAnalyzer([db_action, logaction], r"([^.]*-)?pay[-_]?pa[l1i][-.].*")

wildcard_analyzer = WildcardCertAnalyzer([db_action, logaction]) & X509Analyzer()
letsencrypt_analyzer = LetsEncryptAnalyzer(db_action) & X509Analyzer()

# Set up DNStwist Analyzer - generates a list of potential phishing domains at start. Based on the DNStwist module.
dns = DNStwistAnalyzer(logaction, "paypal.com") & X509Analyzer()

certleak.add_analyzer(dns)
certleak.add_analyzer(xyz_tld_analyzer)
certleak.add_analyzer(phishing_analyzer)
certleak.add_analyzer(regex_analyzer)
certleak.add_analyzer(wildcard_analyzer)
certleak.add_analyzer(letsencrypt_analyzer)

certleak.start()
```

You can find [full example files](https://github.com/d-Rickyy-b/certleak/tree/master/certleak/examples) in this repo as well. 

### License
This tool is released under the MIT license.

If you found this tool helpful and want to support me, drop me a coffee at the link below.

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/0rickyy0)
