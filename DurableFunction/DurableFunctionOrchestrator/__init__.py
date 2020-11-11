# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging

import azure.functions as func
import azure.durable_functions as df
import time


def orchestrator_function(context: df.DurableOrchestrationContext):

    file_name = context.get_input()

    result1 = yield context.call_activity('DurableFunctionActivity', file_name)

    return [file_name] # , result2, result3]

main = df.Orchestrator.create(orchestrator_function)