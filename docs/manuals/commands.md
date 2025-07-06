# Django Commands


## Running Django Commands
```bash
docker compose run cogito python manage.py data_importer <command> <filename>
```


Replace `<command>` with the Django command you want to run.

## Available Subcommands

This command imports member data from a JSON file into the Member model.
```bash
docker compose run cogito python manage.py data_importer import_members old_members.json
```

This command imports member categories from a JSON file into the MemberCategory model.
```bash
docker compose run cogito python manage.py data_importer import_member_categories old_member_categories.json
```

```bash
docker compose run cogito python manage.py data_importer import_member_applications old_member_applications.json
```


```bash
docker compose run cogito python manage.py data_importer import_project_descriptions old_project_descriptions.json
```
