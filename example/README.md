# Example Project with Testiny

1. Configure your Testiny API Key
```shell
# copy the env file
cp example.env .env
# add your key to env file
echo 'key' > .env
```

2. Export our First Case
```shell
turbocase create ./features/web_2/partial.feature.yaml
```
