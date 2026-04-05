#################################################################
## Main Floor Roomba Room Clean Script
#################################################################

        ##########################################################
        ## Region ID / Room Type
        ##########################################################

regions = {
    'USER1_office': {'region_id': '5', 'type': 'rid'},
    'USER2_office': {'region_id': '7', 'type': 'rid'},
    'upstairs_bathroom': {'region_id': '13', 'type': 'rid'},
    'guest_bedroom': {'region_id': '3', 'type': 'rid'},
    'upstairs_hallway': {'region_id': '11', 'type': 'rid'},
    'guest_bathroom': {'region_id': '2', 'type': 'rid'},
    'guest_bedroom_closet': {'region_id': '9', 'type': 'rid'},
    '3d_printer_room': {'region_id': '12', 'type': 'rid'},
    'USER1_office_closet': {'region_id': '10', 'type': 'rid'}
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
if hass.states.get('input_boolean.roomba_clean_upstairs_bathroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_upstairs_bathroom'))
if hass.states.get('input_boolean.roomba_clean_guest_bedroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_guest_bedroom'))
if hass.states.get('input_boolean.roomba_clean_upstairs_hallway').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_upstairs_hallway'))
if hass.states.get('input_boolean.roomba_clean_guest_bathroom').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_guest_bathroom'))
if hass.states.get('input_boolean.roomba_clean_guest_bedroom_closet').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_guest_bedroom_closet'))
if hass.states.get('input_boolean.roomba_clean_3d_printer_room').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_3d_printer_room'))
if hass.states.get('input_boolean.roomba_clean_USER1_office_closet').state == 'on':
    selection_list.append(hass.states.get('input_boolean.roomba_clean_USER1_office_closet'))

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
    if selection == hass.states.get('input_boolean.roomba_clean_upstairs_bathroom'):
        regions_list.append(regions['upstairs_bathroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_guest_bedroom'):
        regions_list.append(regions['guest_bedroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_upstairs_hallway'):
        regions_list.append(regions['upstairs_hallway'])
    if selection == hass.states.get('input_boolean.roomba_clean_guest_bathroom'):
        regions_list.append(regions['guest_bathroom'])
    if selection == hass.states.get('input_boolean.roomba_clean_guest_bedroom_closet'):
        regions_list.append(regions['guest_bedroom_closet'])
    if selection == hass.states.get('input_boolean.roomba_clean_3d_printer_room'):
        regions_list.append(regions['3d_printer_room'])
    if selection == hass.states.get('input_boolean.roomba_clean_USER1_office_closet'):
        regions_list.append(regions['USER1_office_closet'])

        ##########################################################
        ## Clear Input Boolean Selection
        ##########################################################

hass.states.set('input_boolean.roomba_clean_USER1_office', 'off', '')
hass.states.set('input_boolean.roomba_clean_USER2_office', 'off', '')
hass.states.set('input_boolean.roomba_clean_upstairs_bathroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_guest_bedroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_upstairs_hallway', 'off', '')
hass.states.set('input_boolean.roomba_clean_guest_bathroom', 'off', '')
hass.states.set('input_boolean.roomba_clean_guest_bedroom_closet', 'off', '')
hass.states.set('input_boolean.roomba_clean_3d_printer_room', 'off', '')
hass.states.set('input_boolean.roomba_clean_USER1_office_closet', 'off', '')
hass.states.set('input_boolean.upstairs_roomba_room_clean_view', 'off', '')

        ##########################################################
        ## Data to Send
        ##########################################################

service_data = {
    'entity_id': 'vacuum.upstairs',
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