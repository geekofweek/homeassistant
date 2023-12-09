#################################################################
## Basement Roomba Room Clean Script
#################################################################

        ##########################################################
        ## Region ID / Room Type
        ##########################################################

regions = {
    'utility_area': {'region_id': '9', 'type': 'rid'},
    'fitness_room': {'region_id': '5', 'type': 'rid'},
    'craft_room': {'region_id': '1', 'type': 'rid'},
    'laundry_room': {'region_id': '8', 'type': 'rid'},
    'workbench': {'region_id': '7', 'type': 'rid'}
}

        ##########################################################
        ## List Selection
        ##########################################################

selection_list = []
regions_list = []

        ##########################################################
        ## Add Input Boolean to List
        ##########################################################

if hass.states.get('input_boolean.roomba_clean_utility_area').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_utility_area'))
if hass.states.get('input_boolean.roomba_clean_fitness_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_fitness_room'))
if hass.states.get('input_boolean.roomba_clean_craft_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_craft_room'))
if hass.states.get('input_boolean.roomba_clean_laundry_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_laundry_room'))
if hass.states.get('input_boolean.roomba_clean_workbench').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_workbench'))

        ##########################################################
        ## Sort by Timestamp
        ##########################################################

selection_list.sort(key=lambda x:x.last_updated)

        ##########################################################
        ## Add Data to List
        ##########################################################

for selection in selection_list:
    if selection == hass.states.get('input_boolean.roomba_clean_utility_area'):
        regions_list.append(regions['utility_area'])
    if selection == hass.states.get('input_boolean.roomba_clean_fitness_room'):
        regions_list.append(regions['fitness_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_craft_room'):
        regions_list.append(regions['craft_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_laundry_room'):
        regions_list.append(regions['laundry_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_workbench'):
        regions_list.append(regions['workbench'])

        ##########################################################
        ## Clear Input Boolean Selection
        ##########################################################

hass.states.set('input_boolean.roomba_clean_utility_area', 'off', '')
hass.states.set('input_boolean.roomba_clean_fitness_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_craft_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_laundry_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_workbench', 'off', '')

        ##########################################################
        ## Data to Send
        ##########################################################

service_data = {
    'entity_id': 'vacuum.basement_roomba',
    'command': 'start',
    'params': {
        'pmap_id': 'REDACTED',
        'regions': regions_list,
        'ordered': 1,
    }
}

        ##########################################################
        ## Send Command to Roomba
        ##########################################################

hass.services.call('vacuum', 'send_command', service_data, False)