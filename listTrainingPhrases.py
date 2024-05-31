def list_training_phrases(project_id, intent_arr):
    """Returns all training phrases for a specified intent."""

    from google.cloud import dialogflow
    from google.protobuf.json_format import MessageToDict
    import csv

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

        intent = intent_client.get_intent(get_intent_request)
        intent_dict = MessageToDict(intent._pb) # convert response to dictionary

        phrases_arr = []
        fixed_arr = []

        # Iterate through the training phrases.
        for phrases in intent_dict["trainingPhrases"]:
            phrases_arr.append(phrases["parts"])

        for entry in phrases_arr:
            new_dict = merge_list_of_dictionaries(entry)
            fixed_arr.append( ''.join(new_dict["text"]))

        print(fixed_arr)
        csv_arr.append(fixed_arr)
        
    with open('./train_phrases.csv', 'w', encoding='UTF8') as f:

        writer = csv.writer(f)
        for row in csv_arr:
            writer.writerow(row)
# [END dialogflow_list_training_phrases]

# https://stackoverflow.com/questions/45649141/combine-values-of-same-keys-in-a-list-of-dicts
def merge_list_of_dictionaries(dict_list):
  new_dict = {}
  for d in dict_list:
    for d_key in d:
      if d_key not in new_dict:
        new_dict[d_key] = []
      new_dict[d_key].append(d[d_key])
  return new_dict

def list_intents(project_id):
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={"parent": parent})

    intent_arr = []
    intent_to_check = ["Make Appointment", "Hours"] # define your intents here

    for intent in intents:
        if intent.display_name in intent_to_check:
            intent_arr.append(intent.name)

    list_training_phrases(project_id=project_id, intent_arr=intent_arr)

project_id = "banking-ycgr"
list_intents(project_id = project_id)