"""
/taxon/ API endpoints as documented on https://api.obis.org/.
"""
import requests
from urllib.parse import urlencode
from ..obisutils import handle_arrstr, obis_baseurl, obis_GET


class OBISQueryResult:
    def __init__(self):
        """
        An OBISQueryResult object for fetching occurrence records. 
        """
    
    def search(self, scientificname=None, **kwargs):
        """
        Get taxon records.

        :param scientificname: [String,Array] One or more scientific names from the
            OBIS backbone. All included and synonym taxa are included in the search

        :return: A dictionary

        Usage::

            from pyobis import taxa
            taxa.search(scientificname = 'Mola mola')
            taxa.search(scientificname=['Mola mola','Abra alba'])
        """

        scientificname = handle_arrstr(scientificname)
        self.url = obis_baseurl + "taxon/" + scientificname
        self.args = {"scientificname": scientificname}
        out = obis_GET(
            self.url,
            self.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out


    def taxon(self, id, **kwargs):
        """
        Get taxon by ID

        :param id: [Fixnum] An OBIS taxon identifier

        :return: A dictionary

        Usage::

            from pyobis import taxa
            taxa.taxon(545439)
            taxa.taxon(402913)
            taxa.taxon(406296)
            taxa.taxon(415282)
        """
        self.url = obis_baseurl + "taxon/" + str(id)
        self.args = {}
        out = obis_GET(self.url, self.args, "application/json; charset=utf-8", **kwargs)
        return out


    def annotations(self, scientificname, **kwargs):
        """
        Get scientific name annotations by the WoRMS team.

        :param scientificname: [String] Scientific name. Leave empty to include all taxa.
        :return: A dictionary

        Usage::

            from pyobis import taxa
            taxa.annotations(Abra)
        """
        self.url = obis_baseurl + "taxon/annotations"
        scientificname = handle_arrstr(scientificname)
        self.args = {"scientificname": scientificname}
        out = obis_GET(
            self.url,
            self.args,
            "application/json; charset=utf-8",
            **kwargs
        )
        return out
    
    def get_search_url(self):
        """
        Get the corresponding API URL for the query.

        :return: OBIS API URL for the corresponding query

        Usage::

            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            data = query.list(scientificname="Mola mola")
            api_url = query.get_search_url()
            print(api_url)
        """
        return self.url + "?" + urlencode({k:v for k, v in self.args.items() if not v == None})
    
    def get_mapper_url(self):
        """
        Get the corresponding API URL for the query.
        
        :return: OBIS Mapper URL for the corresponding query

        Usage::
        
            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            data = query.list(scientificname="Mola mola")
            api_url = query.get_mapper_url()
            print(api_url)
        """
        if not self.args["taxonid"] and self.args["scientificname"]:
            self.args["taxonid"] = self.lookup_taxon(self.args["scientificname"])[0]["id"]

        return "https://mapper.obis.org/" + "?" + urlencode({k:v for k, v in self.args.items() if not v == None})
    
    def lookup_taxon(self, scientificname):
        """
        Lookup for taxon metadata with scientificname
        
        :param scientificname: [String] Scientific Name

        :return: A dictionary of taxon metadata for the best matches to the input
        Usage::

            from pyobis.checklist import OBISQueryresult as OQR
            query = OQR()
            lookup_data = query.lookup_taxon(scientificname="Mola mola")
            print(lookup_data)
        """
        res = requests.get(f"https://api.obis.org/v3/taxon/complete/{scientificname}")
        return res.json()