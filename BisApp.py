import pickle
from GUI import Application, ScrollableView, Document, Window, Cursor, rgb
from GUI.Files import FileType
from GUI.Geometry import pt_in_rect, offset_rect, rects_intersect
from GUI.StdColors import black, red

class BlobApp(Application):

    def __init__(self):
        Application.__init__(self)
        self.blob_type = FileType(name = "Blob Document", suffix = "blob", 
            #mac_creator = "BLBE", mac_type = "BLOB", # These are optional
        )
        self.file_type = self.blob_type
        self.blob_cursor = Cursor("cursors\\arrow.tiff")
    
    def open_app(self):
        self.new_cmd()

    def make_document(self, fileref):
        return BlobDoc(file_type = self.blob_type)

    def make_window(self, document):
        win = Window(size = (700, 600), document = document)
        view = BlobView(model = document, extent = (1000, 1000), scrolling = 'hv',
            cursor = self.blob_cursor)
        win.place(view, left = 0, top = 0, right = 0, bottom = 0, sticky = 'nsew')
        win.show()