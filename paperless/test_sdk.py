from paperless.client import PaperlessClient
from paperless.objects.customers import AccountList

client = PaperlessClient(
    access_token='93707640df97c7b43c4833dc9d9b3bd2c04cbe27',
    group_slug="integrations-testing",
    base_url="https://release.paperlessparts.com/api"
)
print(AccountList.filter(name="2438"))