

@pytest.fixture
def city() -> City:
    if not City.objects.filter(id=1):
        return City.objects.create(id=1)
