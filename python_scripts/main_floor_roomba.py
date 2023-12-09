#################################################################
## Main Floor Roomba Room Clean Script
#################################################################

        ##########################################################
        ## Region ID / Room Type
        ##########################################################

regions = {
    'living_room': {'region_id': '7', 'type': 'rid'},
    'dining_room': {'region_id': '11', 'type': 'rid'},
    'kitchen': {'region_id': '9', 'type': 'rid'},
    'hallway': {'region_id': '0', 'type': 'rid'},
    'bathroom': {'region_id': '4', 'type': 'rid'},
    'bedroom': {'region_id': '2', 'type': 'rid'},
    'bedroom_closet': {'region_id': '10', 'type': 'rid'},
    'front_door': {'region_id': '1', 'type': 'zid'},
    'back_door': {'region_id': '0', 'type': 'zid'},
    'dining_room_table': {'region_id': '2', 'type': 'zid'}
}

        ##########################################################
        ## List Selection
        ##########################################################

selection_list = []
regions_list = []

        ##########################################################
        ## Add Input Boolean to List
        ##########################################################

if hass.states.get('input_boolean.roomba_clean_living_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_living_room'))
if hass.states.get('input_boolean.roomba_clean_dining_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_dining_room'))
if hass.states.get('input_boolean.roomba_clean_kitchen').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_kitchen'))
if hass.states.get('input_boolean.roomba_clean_hallway').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_hallway'))
if hass.states.get('input_boolean.roomba_clean_bathroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_bathroom'))
if hass.states.get('input_boolean.roomba_clean_bedroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_bedroom'))
if hass.states.get('input_boolean.roomba_clean_bedroom_closet').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_bedroom_closet'))
if hass.states.get('input_boolean.roomba_clean_front_door').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_front_door'))
if hass.states.get('input_boolean.roomba_clean_back_door').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_back_door'))
if hass.states.get('input_boolean.roomba_clean_dining_room_table').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_dining_room_table'))

        ##########################################################
        ## Sort by Timestamp
        ##########################################################

selection_list.sort(key=lambda x:x.last_updated)

        ##########################################################
        ## Data into List Sorted
        ##########################################################

for selection in selection_list:
    if selection == hass.states.get('input_boolean.roomba_clean_living_room'):
        regions_list.append(regions['living_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_dining_room'):
        regions_list.append(regions['dining_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_kitchen'):
        regions_list.append(regions['kitchen'])
    if selection == hass.states.get('input_boolean.roomba_clean_hallway'):
        regions_list.append(regions['hallway'])
    if selection == hass.states.get('input_boolean.roomba_clean_bathroom'):
        regions_list.append(regions['bathroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_bedroom'):
        regions_list.append(regions['bedroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_bedroom_closet'):
        regions_list.append(regions['bedroom_closet'])
    if selection == hass.states.get('input_boolean.roomba_clean_front_door'):
        regions_list.append(regions['front_door'])
    if selection == hass.states.get('input_boolean.roomba_clean_back_door'):
        regions_list.append(regions['back_door'])
    if selection == hass.states.get('input_boolean.roomba_clean_dining_room_table'):
        regions_list.append(regions['dining_room_table'])

        ##########################################################
        ## Clear Input Boolean Selection
        ##########################################################

hass.states.set('input_boolean.roomba_clean_living_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_dining_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_kitchen', 'off', '')
hass.states.set('input_boolean.roomba_clean_hallway', 'off', '')
hass.states.set('input_boolean.roomba_clean_bathroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_bedroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_bedroom_closet', 'off', '')
hass.states.set('input_boolean.roomba_clean_front_door', 'off', '')
hass.states.set('input_boolean.roomba_clean_back_door', 'off', '')
hass.states.set('input_boolean.roomba_clean_dining_room_table', 'off', '')

        ##########################################################
        ## Data to Send
        ##########################################################

service_data = {
    'entity_id': 'vacuum.main_floor_roomba',
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