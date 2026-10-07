docker compose build

docker compose run --rm ansible_tph_runner ansible all -m ping

docker compose run --rm ansible_tph_runner ansible-vault create vault.yml

Example of vault.yml content:

vault_grafana_admin_user: <login>
vault_grafana_admin_password: "<password>"

vault_prometheus_admin_user: <login>
vault_prometheus_admin_password: "<password>"

vault_node_exporter_admin_user: <login>
vault_node_exporter_admin_password: "<password>"


docker compose run --rm ansible_tph_runner ansible-playbook main.yml --ask-vault-pass
