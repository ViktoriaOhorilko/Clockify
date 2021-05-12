## Clockify get task list

####Needed keys

Headers key ` "X-Api-Key" `
contains personal generated API Key (generate it in profile settings 
on your account in `clockify.me` ).

####Functionality description

Function `get_IDs()` gets from response: `https://api.clockify.me/api/v1/user` such IDs:
* `workspaceId` ;
* `userId` ;

Function `get_tasks()` gets from response: 
`https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries` 
existing task(s).

Function `form_data()` creates dictionary with necessary information sorted by key - `date`.

Final function `print_data()` prints information by `stdout` 
and count time by each date and total.
