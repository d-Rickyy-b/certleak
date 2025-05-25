# Analyzers

When CertStream found a new certificate update, it will be passed to all the registered analyzers.
Each analyzer either returns a boolean value, or a list of matches. 

## Available Analyzers

### [AlwaysTrueAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/alwaystrueanalyzer.py)

Analyzer that returns `True` for every certificate update

### [BasicAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/basicanalyzer.py)

Base class for all analyzers

### [CAFingerprintAnalyzer](https://github.com/d-Rickyy-b/certleak/blob/main/certleak/analyzers/cafingerprintanalyzer.py)

Finds certificate updates that are signed by a CA with a specified fingerprint.

### [DNSTwistAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/dnstwistanalyzer.py)

Built on top of [dnstwist](https://github.com/elceef/dnstwist), this analyzer generates lists of permutated domans and matches the domains in each certificate update against them.

### [DomainRegexAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/domainregexanalyzer.py)

Matches a given regex pattern against all the domain names contained in the certificate.

### [FullDomainAnalyzer](https://github.com/d-Rickyy-b/certleak/blob/main/certleak/analyzers/fulldomainanalyzer.py)

Matches certificate updates that contain a specified word.

### [LetsEncryptAnalyzer](https://github.com/d-Rickyy-b/certleak/blob/main/certleak/analyzers/letsencryptanalyzer.py)

Analyzer for finding certificate updates that are signed by Let's Encrypt.

### [PreCertAnalyzer](https://github.com/d-Rickyy-b/certleak/blob/main/certleak/analyzers/precertanalyzer.py)

Finds pre certificate updates. Can be used to exclude precerts.

### [RegexDomainAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/regexdomainanalyzer.py)

Probably the same as "DomainRegexAnalyzer" - TBD

### [SubDomainAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/subdomainanalyzer.py)

Filters certificate updates for certain subdomains. For example the subdomains `imap.` or `blog.`

### [TLDAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/tldanalyzer.py)

Finds certificate updates for domains of given TLDs. For example all domains ending with `.com`.

### [WildcardCertAnalyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/wildcardcertanalyzer.py)

Finds all certificate updates with wildcard domains - For example `*.example.com`.

### [x509Analyzer](https://github.com/d-Rickyy-b/certleak/tree/main/certleak/analyzers/x509analyzer.py)

Not all the certificates are x509 certs. This analyzer fiulters them. Best to be used in combination with other analyzers.

## Combining analyzers

You can combine analyzers logically via AND, OR and a NOT operator.

### AND

Use the ampersand (`&`) char to combine two analyzers with the logical AND operator.

### OR

Use the pipe (`|`) char to combine two analyzers with the logical OR operator.

### NOT

Us the tilde (`~`) char to negate the result of an analyzer.
For example: you want all matches of the TLD `.com` but not the ones matching `example.com`.

```python
dotcomAnalyzer = TLDAnalyzer(actions, ".com")
examplecomAnalyzer = FullDomainAnalyzer(actions=None, contained_words="example.com"):
combined_analyzer = dotcomAnalyzer & ~examplecomAnalyzer
```
