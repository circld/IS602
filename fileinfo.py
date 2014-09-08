"""
Framework for getting filetype-specific metadata

Instantiate appropriate class with filename. Returned object acts like a
dictionary, with key-value pairs for each piece of metadata.
    import fileinfo
    info = fileinfo.MP3FileInfo('C:\Users\Paul\Music\example.mp3')
    print '\\n'.join(['%s=%s' % (k, v) for k, v in info.items()])
Or use listDictionary function to get info on all files in a directory.
    for info in fileinfo.listDirectory('C:\Users\Paul\Music\', ['.mp3']):
        ...

Framework can be extended by adding classes for particular file types, e.g.
HTMLFileInfo, MPGFileInfo, DocFileInfo. Each class is completely responsible
for parsing its files appropriately; see MP3FileInfo for example.
"""
import os
import sys
from UserDict import UserDict


def stripnulls(data):
    """
    :param data: string
    :return: string stripped of whitespace & nulls
    """
    return data.replace('\00', '').strip()


class FileInfo(UserDict):
    """
    Store file metadata
    nb: subclassed to share init with any *FileInfo types to create in future
    """
    def __init__(self, filename=None):
        UserDict.__init__(self)
        self['name'] = filename


class MP3FileInfo(FileInfo):
    """
    Store ID3v1.0 MP3 tags
    """
    tagDataMap = {'title':  ( 3,  33, stripnulls),
                  'artist': ( 33, 63, stripnulls),
                  'album':	( 63, 93, stripnulls),
                  'year':	( 93, 97, stripnulls),
                  'comment':( 97, 126, stripnulls),
                  'genre':	(127, 128, stripnulls)}

    def __parse(self, filename):
        """
        Parse ID3v1.0 tags from MP3 file
        """
        self.clear()
        try:
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()
            if tagdata[:3] == "TAG":
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    self[tag] = parseFunc(tagdata[start:end])
        except IOError:
            pass

    def __setitem__(self, key, item):
        # __setitem__ defines how var[] works
        # if the key is 'name', then __parse is called to extract all tags
        # from the file in question (ie special behavior only if key='name'
        if key == 'name' and item:
            self.__parse(item)
        # calls the *ancestor* __setitem__ (to get 'normal' dict
        # __setitem__ behavior
        FileInfo.__setitem__(self, key, item)


def listDirectory(directory, fileExtList):
    """
    Get list of file info objects for files of particular extensions
    """
    fileList = [os.path.normcase(f)
                for f in os.listdir(directory)]
    fileList = [os.path.join(directory, f)
                for f in fileList
                if os.path.splitext(f)[1] in fileExtList]

    def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):
        """
        Get file info class from filename extension
        """
        subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]
        return hasattr(module, subclass) and getattr(module, subclass) or FileInfo

    return [getFileInfoClass(f)(f) for f in fileList]


if __name__ == '__main__':
    for info in listDirectory('C:\Users\Paul\Music', ['.mp3']):
        print '\n'.join(['%s=%s' % (k, v) for k, v in info.items()])
        print