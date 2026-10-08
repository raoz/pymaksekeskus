# pymaksekeskus
Python library to use Maksekeskus services

## Running the tests

Offline unit tests need no network access or credentials:

```sh
pip install . pytest
pytest
```

The integration tests in `maksekeskus/tests/test_api.py` call the Maksekeskus
**test environment** (`api-test.maksekeskus.ee`). They are skipped unless these
environment variables are set:

| Variable | Value |
| --- | --- |
| `MAKSEKESKUS_SHOP_ID` | Test shop ID |
| `MAKSEKESKUS_SECRET_KEY` | Test shop secret API key |
| `MAKSEKESKUS_PUBLISHABLE_KEY` | Test shop publishable API key |

To run them in GitHub Actions, add the same names as repository secrets
(Settings > Secrets and variables > Actions). Never commit credentials to the
repository.
