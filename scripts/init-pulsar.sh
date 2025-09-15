#!/bin/bash

# Script para inicializar Pulsar con los topics necesarios para Partner Lifecycle Management

echo "Esperando a que Pulsar esté disponible..."
sleep 30

# Crear tenant y namespace
pulsar-admin tenants create partner-lifecycle || echo "Tenant ya existe"
pulsar-admin namespaces create partner-lifecycle/events || echo "Namespace ya existe"

# Crear topics para eventos de partnerships
pulsar-admin topics create persistent://partner-lifecycle/events/partner-events || echo "Topic partner-events ya existe"

echo "Inicialización de Pulsar completada para Partner Lifecycle Management"
