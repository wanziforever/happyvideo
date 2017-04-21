
from settings import settings

# now, just do a basic round-robin pick
# in the future:
# consider add weight to solrs, for example, give the local solr higher priority
# consider add keep-alive check.

class SolrRouter(object):
    def __init__(self, solrs):
        #solrs='1.1.1.1:222,192.1.1.1:33'
        self._solrs = [ s.replace(' ','') for s in solrs.split(',')]
        self._idx = 0
        self._size = len(self._solrs)

    def pick(self):
        solr = self._solrs[self._idx]
        self._idx = (self._idx + 1 ) % self._size
        return solr

    def get_all(self):
        return self._solrs

solr_router = SolrRouter(settings.SOLR_SERVERS)
