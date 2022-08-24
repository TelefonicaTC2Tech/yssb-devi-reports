# yssb-devi-reports

Custom Devi reports for Your Smart and Secure Business (YSSB).

## Development environment

Before launching the development environment, you need a valid Devi API Key. This API key is required to test the report generation against a real Devi instance.

Launch the development environment:

```
# Export devi apikey
export DEVI_APIKEY="ApiKey SU-XXX-XXX-XXX:XXXXXXXXX"

# Start up the development environment
make develenv-up

# Open a shell to the development environment
make develenv-sh
```

Within a shell of the development environment, all the dependencies are installed.

```
# Launch unit tests
make test
```

Withing the shell, it is possible to interact with Devi to list the available reports and generate reports with real data:

```
# Add the Devi account. 
# The environment variable DEVI_APIKEY needs to target a valid api key
make devi-account

# List the reports provided by this repository
make devi-reports

# Generate a params report
make devi-report-params

# Generate a fulfillment report
make devi-report-fulfillment

# Generate an inquiring report
make devi-report-inquiring

# Generate an EU funds report
make devi-report-eufunds
```

## Managing reports in Devi

### Adding a repository

Note that this step need to be done only once.

Steps:

- Access to Devi connect site and navigate to [Account > Reports > Repositories](https://vendor.connect.telefonicacloud.com/account/reports/repositories).
- Press the link `ADD REPOSITORY` to add this repository.
- Fill the form:
  - Git Repository URL: https://github.com/TelefonicaTC2Tech/yssb-devi-reports
  - Enable `Requires authorization` because the git repository is private:
    - Username: Add the username
    - Personal Access Token: Add the personal access token with read permissions for this repository.
- Press next and choose the tag
- Complete the wizard.

### Editing a repository

Steps:

- Access to Devi connect site and navigate to [Account > Reports > Repositories](https://vendor.connect.telefonicacloud.com/account/reports/repositories).
- Press the edit button (pencil icon) to edit one of the repositories of the list.
- Complete the form as indicated in `Adding a repository` section.

### Create a report

Steps:

- Access to Devi connect site and navigate to [Reports](https://vendor.connect.telefonicacloud.com/reports/directory).
- Press the link `CREATE REPORT`.
- Select one of the templates of this repository. Possible templates are: `Fulfillment requests report (TaxID)` or `Inquiring requests`.
- Complete the wizard specific for the selected template.
