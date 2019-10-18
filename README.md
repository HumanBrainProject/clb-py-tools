# clb-py-tools

This Python package contains helpers that are provided with the Collaboratory to help
with integration in the Collaboratory.

They following packages are provided:

- iam: Tools to interact with the IAM service to obtain tokens and manage users' teams,
  groups, accreditations and units.

## The Collaboratory

The [Collaboratory](https://wiki.humanbrainproject.eu/) is a platform provided by the HBP
as a gateway to the infrastructure built by the project, perform research, facilitate
collaboration within the project, as well as dissemination and teaching.

## Installation

To install the package run

```
pip install clb-py-tools
```

## Usage

### iam

#### Client

The `Client` interacts with the IAM provider

```
from clb_py_tools.iam.client import Client
```

Refreshing a token:
```
access_token = Client.refresh_access_token(client_id, client_secret, oauth)
```

The `Identity`

```
from clb_py_tools.iam.identity import Identity
```

Obtaining the userinfo
```
identity = Identity(token)

identity.refresh()
identity.sync()

identity.userinfo
identity.teams
identity.groups
identity.units
identity.accreditations
identity.roles
```
