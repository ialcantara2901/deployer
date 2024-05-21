import pika
import json
import os
import subprocess

def deploy_stack(stack_name, stack_file_content):
    # Escreve o conteúdo do stack file em um arquivo temporário
    stack_file_path = f"/tmp/{stack_name}.yaml"
    with open(stack_file_path, 'w') as stack_file:
        stack_file.write(stack_file_content)

    # Executa o comando Docker stack deploy
    command = f"docker stack deploy -c {stack_file_path} {stack_name}"
    result = subprocess.run(command, shell=True, capture_output=True)

    if result.returncode != 0:
        print(f"Erro ao fazer deploy da stack: {result.stderr.decode()}")
    else:
        print(f"Deploy da stack {stack_name} realizado com sucesso.")

def callback(ch, method, properties, body):
    data = json.loads(body)
    stack_name = data.get('stack_name')
    stack_file_content = data.get('stack_file_content')

    if stack_name and stack_file_content:
        deploy_stack(stack_name, stack_file_content)
    else:
        print("JSON inválido: faltando 'stack_name' ou 'stack_file_content'.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbitmq_queue = os.getenv('RABBITMQ_QUEUE', 'deployments')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue, durable=True)
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback)

    print('Aguardando mensagens...')
    channel.start_consuming()

if __name__ == "__main__":
    main()
