#################################################################
## Upstairs Roomba Room Clean Script
#################################################################

        ##########################################################
        ## Region ID / Room Type
        ##########################################################

regions = {
    'media_room': {'region_id': '12', 'type': 'rid'},
    'game_room': {'region_id': '14', 'type': 'rid'},
    'basement_bathroom': {'region_id': '10', 'type': 'rid'},
    'fitness_room': {'region_id': '13', 'type': 'rid'},
    'basement_storage': {'region_id': '5', 'type': 'rid'}
}

        ##########################################################
        ## List Selection
        ##########################################################

selection_list = []
regions_list = []

        ##########################################################
        ## Add Input Boolean to List
        ##########################################################

if hass.states.get('input_boolean.roomba_clean_media_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_media_room'))
if hass.states.get('input_boolean.roomba_clean_game_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_game_room'))
if hass.states.get('input_boolean.roomba_clean_basement_bathroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_basement_bathroom'))
if hass.states.get('input_boolean.roomba_clean_fitness_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_fitness_room'))
if hass.states.get('input_boolean.roomba_clean_basement_storage').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_basement_storage'))

        ##########################################################
        ## Sort by Timestamp
        ##########################################################

selection_list.sort(key=lambda x:x.last_updated)

        ##########################################################
        ## Data into List Sorted
        ##########################################################

for selection in selection_list:
    if selection == hass.states.get('input_boolean.roomba_clean_media_room'):
        regions_list.append(regions['media_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_game_room'):
        regions_list.append(regions['game_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_basement_bathroom'):
        regions_list.append(regions['basement_bathroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_fitness_room'):
        regions_list.append(regions['fitness_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_basement_storage'):
        regions_list.append(regions['basement_storage'])

        ##########################################################
        ## Clear Input Boolean Selection
        ##########################################################

hass.states.set('input_boolean.roomba_clean_media_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_game_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_basement_bathroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_fitness_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_basement_storage', 'off', '')
hass.states.set('input_boolean.basement_roomba_room_clean_view', 'off', '')

        ##########################################################
        ## Data to Send
        ##########################################################

service_data = {
    'entity_id': 'vacuum.basement',
    'command': 'start',
    'params': {
        'pmap_id': 'OfbQnX7uQ_qjgHzYYSFdkQ',
        'regions': regions_list,
        'ordered': 1,
    }
}

        ##########################################################
        ## Send Command to Roomba
        ##########################################################

hass.services.call('vacuum', 'send_command', service_data, False)