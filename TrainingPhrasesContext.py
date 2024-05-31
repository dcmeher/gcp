import csv
import xlwt
from google.cloud import dialogflow
import json
from google.protobuf.json_format import MessageToDict

def list_training_phrases(project_id, intent_arr):
    """Returns all training phrases for a specified intent."""
     # Create a new workbook and add a worksheet
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Training Phrases')

    # Write headers
    worksheet.write(0, 0, 'Intent Display Name')
    worksheet.write(0, 1, 'Training Phrase')
    worksheet.write(0, 2, 'Context')

    row = 1  # Start from the second row

    # Create the intents client
    intent_client = dialogflow.IntentsClient()

    # The options for views of an intent
    intent_view = dialogflow.IntentView.INTENT_VIEW_FULL

    # Compose the get-intent request
    csv_arr = []

    for intent_name in intent_arr:
        get_intent_request = dialogflow.GetIntentRequest(
            name=intent_name, intent_view=intent_view
        )
        
        intent = intent_client.get_intent(request=get_intent_request)
        intent_display_name = intent.display_name
        #print(intent)
        #associated_contexts = [context.name for context in intent.input_context_names]
        associated_contexts =[]
        for context in intent.input_context_names:
             associated_contexts =''.join(context)

        #print(associated_contexts)
        training_phrases_text = []
        # Iterate over training phrases of the intent
        for training_phrase in intent.training_phrases:
             # Iterate over parts of the training phrase
            parts_text = []
            for part in training_phrase.parts:
                parts_text.append(part.text)
            # Join parts to form the complete training phrase text
            training_phrase_text = ''.join(parts_text)
            training_phrases_text.append(training_phrase_text)
            # Now training_phrases_text contains the text of all training phrases
            # Write data to Excel file
            worksheet.write(row, 0, intent_display_name)
            worksheet.write(row, 1, training_phrase_text)
            worksheet.write(row, 2, associated_contexts)
           # print(training_phrases_text)
            row += 1
# Save the workbook to a file
    workbook.save('./training_phrases_context.xls')
    print("Training phrases have been written to 'training_phrases.xls'.")

def list_intents(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = f"projects/{project_id}/agent"
    intents = intents_client.list_intents(request={"parent": parent})
   # print(intents)
    intent_arr = []
    #intent_to_check = ["PaymentDeferment", "ExtendLease"]  # define your intents here

    for intent in intents:
       # if intent.display_name in intent_to_check:
            intent_arr.append(intent.name)
    list_training_phrases(project_id=project_id, intent_arr=intent_arr)

project_id = "banking-ycgr"
list_intents(project_id=project_id)