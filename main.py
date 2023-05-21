import utils.database_handler as dh
import utils.remote_db_handler as rh
from GUI.gui import App

rh.RemoteDB.init_remote_tables()
th = dh.TableHandler()
file_list = th.get_file_uploads()
app = App(token=th.auth_token, file_list=file_list)
app.monitor_local_update()
app.mainloop()