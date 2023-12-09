#################################################################
## Upstairs Roomba Room Clean Script
#################################################################

        ##########################################################
        ## Region ID / Room Type
        ##########################################################

regions = {
    'USER1_office': {'region_id': '2', 'type': 'rid'},
    'USER2_office': {'region_id': '7', 'type': 'rid'},
    'guest_bedroom': {'region_id': '1', 'type': 'rid'},
    'upstairs_hallway': {'region_id': '8', 'type': 'rid'}
}

        ##########################################################
        ## List Selection
        ##########################################################

selection_list = []
regions_list = []

        ##########################################################
        ## Add Input Boolean to List
        ##########################################################

if hass.states.get('input_boolean.roomba_clean_USER1_office').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_USER1_office'))
if hass.states.get('input_boolean.roomba_clean_USER2_office').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_USER2_office'))
if hass.states.get('input_boolean.roomba_clean_guest_bedroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_guest_bedroom'))
if hass.states.get('input_boolean.roomba_clean_upstairs_hallway').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_upstairs_hallway'))

        ##########################################################
        ## Sort by Timestamp
        ##########################################################

selection_list.sort(key=lambda x:x.last_updated)

        ##########################################################
        ## Data into List Sorted
        ##########################################################

for selection in selection_list:
    if selection == hass.states.get('input_boolean.roomba_clean_USER1_office'):
        regions_list.append(regions['USER1_office'])
    if selection == hass.states.get('input_boolean.roomba_clean_USER2_office'):
        regions_list.append(regions['USER2_office'])
    if selection == hass.states.get('input_boolean.roomba_clean_guest_bedroom'):
        regions_list.append(regions['guest_bedroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_upstairs_hallway'):
        regions_list.append(regions['upstairs_hallway'])

        ##########################################################
        ## Clear Input Boolean Selection
        ##########################################################

hass.states.set('input_boolean.roomba_clean_USER1_office', 'off', '')
hass.states.set('input_boolean.roomba_clean_USER2_office', 'off', '')
hass.states.set('input_boolean.roomba_clean_guest_bedroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_upstairs_hallway', 'off', '')

        ##########################################################
        ## Data to Send
        ##########################################################

service_data = {
    'entity_id': 'vacuum.upstairs_roomba',
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