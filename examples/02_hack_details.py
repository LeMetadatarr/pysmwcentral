"""Look up a single hack by its numeric id."""
import pysmwcentral

hack = pysmwcentral.get_hack(42415)
print("name:      ", hack.name)
print("authors:   ", ", ".join(hack.author_names))
print("section:   ", hack.section)
print("type:      ", hack.type)
print("difficulty:", hack.difficulty)
print("length:    ", hack.length, "exit(s)")
print("rating:    ", hack.rating)
print("downloads: ", hack.downloads)
print("tags:      ", hack.tags)
print("url:       ", hack.url)
print("download:  ", hack.download_url)
