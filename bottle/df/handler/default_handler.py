#!/usr/bin/env python

from sqlalchemy.orm.exc import NoResultFound
from ..datamodel.schema import SCHEMA, DATATYPE
from base_handler import db_handler
from common.dbutil import slice_query
from ..exceptions import NoSupportDataType
from ..data_descriptor import InvalidKeyException
    
class basic_vender_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_vender_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_vender_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_vender).filter(basic_vender.id==id).all()
                else:
                    q = self.session.query(basic_vender).filter(basic_vender.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_vender).all()
                else:
                    q = self.session.query(basic_vender)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_vender donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_vender_handler", "id")
            try:
                self.session.query(basic_vender).filter(basic_vender.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_vender(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_vender instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_vender process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_vender process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_vender_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_vender_handler", "id")
            try:
                ret = self.session.query(basic_vender).filter(basic_vender.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_vender).count()
                return ret
            except NoResultFound, e:
                print "basic_vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_vender donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_vender_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_vender_handler", "id")
            try:
                self.session.query(basic_vender).filter(basic_vender.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class vender_attr_mapping_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(vender_attr_mapping_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type).all()
                else:
                    q = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(vender_attr_mapping).all()
                else:
                    q = self.session.query(vender_attr_mapping)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vender_attr_mapping donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = vender_attr_mapping(**self.data_desc.modifier)
            except:
                print "fail to initialize the vender_attr_mapping instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "vender_attr_mapping process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "vender_attr_mapping process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("vender_attr_mapping_handler", "vender_id")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_type == data_type:
            try:
                type = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: type parameters is required for data_type_all_bytype"
                raise InvalidKeyException("vender_attr_mapping_handler", "type")
            try:
                ret = self.session.query(vender_attr_mapping).filter(vender_attr_mapping.type==type).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_type"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(vender_attr_mapping).count()
                return ret
            except NoResultFound, e:
                print "vender_attr_mapping_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "vender_attr_mapping donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import vender_attr_mapping
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "vender_attr_mapping_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("vender_attr_mapping_handler", "id")
            try:
                self.session.query(vender_attr_mapping).filter(vender_attr_mapping.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "vender_attr_mapping_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class oss_user_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(oss_user_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).filter(oss_user.id==id).all()
                else:
                    q = self.session.query(oss_user).filter(oss_user.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_staffId == data_type:
            try:
                staffId = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "staffId")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).filter(oss_user.staffId==staffId).all()
                else:
                    q = self.session.query(oss_user).filter(oss_user.staffId==staffId)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_staffId"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_user).all()
                else:
                    q = self.session.query(oss_user)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_user donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                self.session.query(oss_user).filter(oss_user.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "oss_user_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = oss_user(**self.data_desc.modifier)
            except:
                print "fail to initialize the oss_user instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "oss_user process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "oss_user process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                ret = self.session.query(oss_user).filter(oss_user.id==id).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_staffId == data_type:
            try:
                staffId = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: staffId parameters is required for data_type_all_bystaffId"
                raise InvalidKeyException("oss_user_handler", "staffId")
            try:
                ret = self.session.query(oss_user).filter(oss_user.staffId==staffId).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_all_by_staffId"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(oss_user).count()
                return ret
            except NoResultFound, e:
                print "oss_user_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_user donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import oss_user
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_user_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("oss_user_handler", "id")
            try:
                self.session.query(oss_user).filter(oss_user.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "oss_user_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class medias_update_record_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(medias_update_record_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).filter(medias_update_record.id==id).all()
                else:
                    q = self.session.query(medias_update_record).filter(medias_update_record.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id).all()
                else:
                    q = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(medias_update_record).all()
                else:
                    q = self.session.query(medias_update_record)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "medias_update_record donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                self.session.query(medias_update_record).filter(medias_update_record.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "medias_update_record_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = medias_update_record(**self.data_desc.modifier)
            except:
                print "fail to initialize the medias_update_record instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "medias_update_record process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "medias_update_record process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                ret = self.session.query(medias_update_record).filter(medias_update_record.id==id).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("medias_update_record_handler", "media_id")
            try:
                ret = self.session.query(medias_update_record).filter(medias_update_record.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(medias_update_record).count()
                return ret
            except NoResultFound, e:
                print "medias_update_record_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "medias_update_record donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import medias_update_record
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "medias_update_record_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("medias_update_record_handler", "id")
            try:
                self.session.query(medias_update_record).filter(medias_update_record.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "medias_update_record_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class basic_category_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_category_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_category_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_category).filter(basic_category.id==id).all()
                else:
                    q = self.session.query(basic_category).filter(basic_category.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_parent_id == data_type:
            try:
                parent_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_category_handler", "parent_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_category).filter(basic_category.parent_id==parent_id).all()
                else:
                    q = self.session.query(basic_category).filter(basic_category.parent_id==parent_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_parent_id"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_category_handler", "is_sync")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_category).filter(basic_category.is_sync==is_sync).all()
                else:
                    q = self.session.query(basic_category).filter(basic_category.is_sync==is_sync)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_category).all()
                else:
                    q = self.session.query(basic_category)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_category donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_category_handler", "id")
            try:
                self.session.query(basic_category).filter(basic_category.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_category(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_category instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_category process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_category process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_category_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_category_handler", "id")
            try:
                ret = self.session.query(basic_category).filter(basic_category.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_parent_id == data_type:
            try:
                parent_id = self.data_desc.getKey(1)
            except:
                print "basic_category_handler: parent_id parameters is required for data_type_all_byparent_id"
                raise InvalidKeyException("basic_category_handler", "parent_id")
            try:
                ret = self.session.query(basic_category).filter(basic_category.parent_id==parent_id).count()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_parent_id"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                print "basic_category_handler: is_sync parameters is required for data_type_all_byis_sync"
                raise InvalidKeyException("basic_category_handler", "is_sync")
            try:
                ret = self.session.query(basic_category).filter(basic_category.is_sync==is_sync).count()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_category).count()
                return ret
            except NoResultFound, e:
                print "basic_category_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_category donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_category
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_category_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_category_handler", "id")
            try:
                self.session.query(basic_category).filter(basic_category.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_category_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class basic_media_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_media_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.id==id).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_title == data_type:
            try:
                title = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "title")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.title==title).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.title==title)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_title"
                raise e
    
        elif DATATYPE.data_type_all_by_available == data_type:
            try:
                available = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "available")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.available==available).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.available==available)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_available"
                raise e
    
        elif DATATYPE.data_type_all_by_fee == data_type:
            try:
                fee = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "fee")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.fee==fee).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.fee==fee)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_fee"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "category_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.category_id==category_id).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.category_id==category_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_all_by_button_name == data_type:
            try:
                button_name = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "button_name")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.button_name==button_name).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.button_name==button_name)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_button_name"
                raise e
    
        elif DATATYPE.data_type_all_by_show_detail == data_type:
            try:
                show_detail = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "show_detail")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.show_detail==show_detail).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.show_detail==show_detail)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_show_detail"
                raise e
    
        elif DATATYPE.data_type_all_by_site_status == data_type:
            try:
                site_status = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "site_status")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.site_status==site_status).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.site_status==site_status)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_site_status"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "is_sync")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).filter(basic_media.is_sync==is_sync).all()
                else:
                    q = self.session.query(basic_media).filter(basic_media.is_sync==is_sync)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_media).all()
                else:
                    q = self.session.query(basic_media)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_media donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_media_handler", "id")
            try:
                self.session.query(basic_media).filter(basic_media.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_media(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_media instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_media process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_media process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_media_handler", "id")
            try:
                ret = self.session.query(basic_media).filter(basic_media.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_title == data_type:
            try:
                title = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: title parameters is required for data_type_all_bytitle"
                raise InvalidKeyException("basic_media_handler", "title")
            try:
                ret = self.session.query(basic_media).filter(basic_media.title==title).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_title"
                raise e
    
        elif DATATYPE.data_type_all_by_available == data_type:
            try:
                available = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: available parameters is required for data_type_all_byavailable"
                raise InvalidKeyException("basic_media_handler", "available")
            try:
                ret = self.session.query(basic_media).filter(basic_media.available==available).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_available"
                raise e
    
        elif DATATYPE.data_type_all_by_fee == data_type:
            try:
                fee = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: fee parameters is required for data_type_all_byfee"
                raise InvalidKeyException("basic_media_handler", "fee")
            try:
                ret = self.session.query(basic_media).filter(basic_media.fee==fee).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_fee"
                raise e
    
        elif DATATYPE.data_type_all_by_category_id == data_type:
            try:
                category_id = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: category_id parameters is required for data_type_all_bycategory_id"
                raise InvalidKeyException("basic_media_handler", "category_id")
            try:
                ret = self.session.query(basic_media).filter(basic_media.category_id==category_id).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_category_id"
                raise e
    
        elif DATATYPE.data_type_all_by_button_name == data_type:
            try:
                button_name = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: button_name parameters is required for data_type_all_bybutton_name"
                raise InvalidKeyException("basic_media_handler", "button_name")
            try:
                ret = self.session.query(basic_media).filter(basic_media.button_name==button_name).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_button_name"
                raise e
    
        elif DATATYPE.data_type_all_by_show_detail == data_type:
            try:
                show_detail = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: show_detail parameters is required for data_type_all_byshow_detail"
                raise InvalidKeyException("basic_media_handler", "show_detail")
            try:
                ret = self.session.query(basic_media).filter(basic_media.show_detail==show_detail).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_show_detail"
                raise e
    
        elif DATATYPE.data_type_all_by_site_status == data_type:
            try:
                site_status = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: site_status parameters is required for data_type_all_bysite_status"
                raise InvalidKeyException("basic_media_handler", "site_status")
            try:
                ret = self.session.query(basic_media).filter(basic_media.site_status==site_status).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_site_status"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: is_sync parameters is required for data_type_all_byis_sync"
                raise InvalidKeyException("basic_media_handler", "is_sync")
            try:
                ret = self.session.query(basic_media).filter(basic_media.is_sync==is_sync).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_media).count()
                return ret
            except NoResultFound, e:
                print "basic_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_media donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_media_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_media_handler", "id")
            try:
                self.session.query(basic_media).filter(basic_media.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class basic_program_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_program_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_program
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.id==id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.media_id==media_id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.vender_id==vender_id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_media_source_id == data_type:
            try:
                ref_media_source_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "ref_media_source_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.ref_media_source_id==ref_media_source_id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.ref_media_source_id==ref_media_source_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_parent_media_source_id == data_type:
            try:
                ref_parent_media_source_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "ref_parent_media_source_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.ref_parent_media_source_id==ref_parent_media_source_id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.ref_parent_media_source_id==ref_parent_media_source_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_parent_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_program_source_id == data_type:
            try:
                ref_program_source_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "ref_program_source_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).filter(basic_program.ref_program_source_id==ref_program_source_id).all()
                else:
                    q = self.session.query(basic_program).filter(basic_program.ref_program_source_id==ref_program_source_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_program_source_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_program).all()
                else:
                    q = self.session.query(basic_program)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_program donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_program
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_program_handler", "id")
            try:
                self.session.query(basic_program).filter(basic_program.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_program_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_program
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_program(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_program instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_program process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_program process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_program
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_program_handler", "id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("basic_program_handler", "media_id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("basic_program_handler", "vender_id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_media_source_id == data_type:
            try:
                ref_media_source_id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: ref_media_source_id parameters is required for data_type_all_byref_media_source_id"
                raise InvalidKeyException("basic_program_handler", "ref_media_source_id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.ref_media_source_id==ref_media_source_id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_parent_media_source_id == data_type:
            try:
                ref_parent_media_source_id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: ref_parent_media_source_id parameters is required for data_type_all_byref_parent_media_source_id"
                raise InvalidKeyException("basic_program_handler", "ref_parent_media_source_id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.ref_parent_media_source_id==ref_parent_media_source_id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_parent_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_program_source_id == data_type:
            try:
                ref_program_source_id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: ref_program_source_id parameters is required for data_type_all_byref_program_source_id"
                raise InvalidKeyException("basic_program_handler", "ref_program_source_id")
            try:
                ret = self.session.query(basic_program).filter(basic_program.ref_program_source_id==ref_program_source_id).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_all_by_ref_program_source_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_program).count()
                return ret
            except NoResultFound, e:
                print "basic_program_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_program donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_program
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_program_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_program_handler", "id")
            try:
                self.session.query(basic_program).filter(basic_program.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_program_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class audit_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(audit_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import audit
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("audit_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(audit).filter(audit.id==id).all()
                else:
                    q = self.session.query(audit).filter(audit.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_review_time == data_type:
            try:
                review_time = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("audit_handler", "review_time")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(audit).filter(audit.review_time==review_time).all()
                else:
                    q = self.session.query(audit).filter(audit.review_time==review_time)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_review_time"
                raise e
    
        elif DATATYPE.data_type_all_by_audit_time == data_type:
            try:
                audit_time = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("audit_handler", "audit_time")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(audit).filter(audit.audit_time==audit_time).all()
                else:
                    q = self.session.query(audit).filter(audit.audit_time==audit_time)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_audit_time"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(audit).all()
                else:
                    q = self.session.query(audit)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "audit donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import audit
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("audit_handler", "id")
            try:
                self.session.query(audit).filter(audit.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "audit_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import audit
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = audit(**self.data_desc.modifier)
            except:
                print "fail to initialize the audit instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "audit process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "audit process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import audit
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "audit_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("audit_handler", "id")
            try:
                ret = self.session.query(audit).filter(audit.id==id).count()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_review_time == data_type:
            try:
                review_time = self.data_desc.getKey(1)
            except:
                print "audit_handler: review_time parameters is required for data_type_all_byreview_time"
                raise InvalidKeyException("audit_handler", "review_time")
            try:
                ret = self.session.query(audit).filter(audit.review_time==review_time).count()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_review_time"
                raise e
    
        elif DATATYPE.data_type_all_by_audit_time == data_type:
            try:
                audit_time = self.data_desc.getKey(1)
            except:
                print "audit_handler: audit_time parameters is required for data_type_all_byaudit_time"
                raise InvalidKeyException("audit_handler", "audit_time")
            try:
                ret = self.session.query(audit).filter(audit.audit_time==audit_time).count()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_all_by_audit_time"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(audit).count()
                return ret
            except NoResultFound, e:
                print "audit_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "audit donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import audit
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "audit_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("audit_handler", "id")
            try:
                self.session.query(audit).filter(audit.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "audit_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class site_system_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(site_system_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import site_system
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("site_system_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(site_system).filter(site_system.id==id).all()
                else:
                    q = self.session.query(site_system).filter(site_system.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "site_system_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(site_system).all()
                else:
                    q = self.session.query(site_system)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "site_system_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "site_system donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import site_system
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("site_system_handler", "id")
            try:
                self.session.query(site_system).filter(site_system.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "site_system_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import site_system
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = site_system(**self.data_desc.modifier)
            except:
                print "fail to initialize the site_system instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "site_system process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "site_system process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import site_system
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "site_system_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("site_system_handler", "id")
            try:
                ret = self.session.query(site_system).filter(site_system.id==id).count()
                return ret
            except NoResultFound, e:
                print "site_system_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(site_system).count()
                return ret
            except NoResultFound, e:
                print "site_system_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "site_system donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import site_system
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "site_system_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("site_system_handler", "id")
            try:
                self.session.query(site_system).filter(site_system.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "site_system_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class rule_vender_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(rule_vender_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import rule_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_vender_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_vender).filter(rule_vender.id==id).all()
                else:
                    q = self.session.query(rule_vender).filter(rule_vender.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_vender).all()
                else:
                    q = self.session.query(rule_vender)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "rule_vender donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import rule_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_vender_handler", "id")
            try:
                self.session.query(rule_vender).filter(rule_vender.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "rule_vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import rule_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = rule_vender(**self.data_desc.modifier)
            except:
                print "fail to initialize the rule_vender instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "rule_vender process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "rule_vender process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import rule_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "rule_vender_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("rule_vender_handler", "id")
            try:
                ret = self.session.query(rule_vender).filter(rule_vender.id==id).count()
                return ret
            except NoResultFound, e:
                print "rule_vender_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(rule_vender).count()
                return ret
            except NoResultFound, e:
                print "rule_vender_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "rule_vender donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import rule_vender
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "rule_vender_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("rule_vender_handler", "id")
            try:
                self.session.query(rule_vender).filter(rule_vender.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "rule_vender_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class rule_media_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(rule_media_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import rule_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_media_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_media).filter(rule_media.id==id).all()
                else:
                    q = self.session.query(rule_media).filter(rule_media.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_media_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_media).filter(rule_media.vender_id==vender_id).all()
                else:
                    q = self.session.query(rule_media).filter(rule_media.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_media_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_media).filter(rule_media.media_id==media_id).all()
                else:
                    q = self.session.query(rule_media).filter(rule_media.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(rule_media).all()
                else:
                    q = self.session.query(rule_media)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "rule_media donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import rule_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("rule_media_handler", "id")
            try:
                self.session.query(rule_media).filter(rule_media.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "rule_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import rule_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = rule_media(**self.data_desc.modifier)
            except:
                print "fail to initialize the rule_media instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "rule_media process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "rule_media process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import rule_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "rule_media_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("rule_media_handler", "id")
            try:
                ret = self.session.query(rule_media).filter(rule_media.id==id).count()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "rule_media_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("rule_media_handler", "vender_id")
            try:
                ret = self.session.query(rule_media).filter(rule_media.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "rule_media_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("rule_media_handler", "media_id")
            try:
                ret = self.session.query(rule_media).filter(rule_media.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(rule_media).count()
                return ret
            except NoResultFound, e:
                print "rule_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "rule_media donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import rule_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "rule_media_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("rule_media_handler", "id")
            try:
                self.session.query(rule_media).filter(rule_media.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "rule_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class import_history_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(import_history_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import import_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("import_history_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(import_history).filter(import_history.id==id).all()
                else:
                    q = self.session.query(import_history).filter(import_history.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("import_history_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(import_history).filter(import_history.vender_id==vender_id).all()
                else:
                    q = self.session.query(import_history).filter(import_history.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("import_history_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(import_history).filter(import_history.media_id==media_id).all()
                else:
                    q = self.session.query(import_history).filter(import_history.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_username == data_type:
            try:
                username = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("import_history_handler", "username")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(import_history).filter(import_history.username==username).all()
                else:
                    q = self.session.query(import_history).filter(import_history.username==username)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_username"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(import_history).all()
                else:
                    q = self.session.query(import_history)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "import_history donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import import_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("import_history_handler", "id")
            try:
                self.session.query(import_history).filter(import_history.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "import_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import import_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = import_history(**self.data_desc.modifier)
            except:
                print "fail to initialize the import_history instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "import_history process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "import_history process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import import_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "import_history_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("import_history_handler", "id")
            try:
                ret = self.session.query(import_history).filter(import_history.id==id).count()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "import_history_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("import_history_handler", "vender_id")
            try:
                ret = self.session.query(import_history).filter(import_history.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "import_history_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("import_history_handler", "media_id")
            try:
                ret = self.session.query(import_history).filter(import_history.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_username == data_type:
            try:
                username = self.data_desc.getKey(1)
            except:
                print "import_history_handler: username parameters is required for data_type_all_byusername"
                raise InvalidKeyException("import_history_handler", "username")
            try:
                ret = self.session.query(import_history).filter(import_history.username==username).count()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_all_by_username"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(import_history).count()
                return ret
            except NoResultFound, e:
                print "import_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "import_history donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import import_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "import_history_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("import_history_handler", "id")
            try:
                self.session.query(import_history).filter(import_history.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "import_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class hot_media_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(hot_media_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import hot_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).filter(hot_media.id==id).all()
                else:
                    q = self.session.query(hot_media).filter(hot_media.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).filter(hot_media.vender_id==vender_id).all()
                else:
                    q = self.session.query(hot_media).filter(hot_media.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_media_source_id == data_type:
            try:
                ref_media_source_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "ref_media_source_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).filter(hot_media.ref_media_source_id==ref_media_source_id).all()
                else:
                    q = self.session.query(hot_media).filter(hot_media.ref_media_source_id==ref_media_source_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_ref_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "media_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).filter(hot_media.media_id==media_id).all()
                else:
                    q = self.session.query(hot_media).filter(hot_media.media_id==media_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_finished == data_type:
            try:
                finished = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "finished")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).filter(hot_media.finished==finished).all()
                else:
                    q = self.session.query(hot_media).filter(hot_media.finished==finished)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_finished"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(hot_media).all()
                else:
                    q = self.session.query(hot_media)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "hot_media donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import hot_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("hot_media_handler", "id")
            try:
                self.session.query(hot_media).filter(hot_media.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "hot_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import hot_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = hot_media(**self.data_desc.modifier)
            except:
                print "fail to initialize the hot_media instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "hot_media process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "hot_media process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import hot_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("hot_media_handler", "id")
            try:
                ret = self.session.query(hot_media).filter(hot_media.id==id).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("hot_media_handler", "vender_id")
            try:
                ret = self.session.query(hot_media).filter(hot_media.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_ref_media_source_id == data_type:
            try:
                ref_media_source_id = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: ref_media_source_id parameters is required for data_type_all_byref_media_source_id"
                raise InvalidKeyException("hot_media_handler", "ref_media_source_id")
            try:
                ret = self.session.query(hot_media).filter(hot_media.ref_media_source_id==ref_media_source_id).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_ref_media_source_id"
                raise e
    
        elif DATATYPE.data_type_all_by_media_id == data_type:
            try:
                media_id = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: media_id parameters is required for data_type_all_bymedia_id"
                raise InvalidKeyException("hot_media_handler", "media_id")
            try:
                ret = self.session.query(hot_media).filter(hot_media.media_id==media_id).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_media_id"
                raise e
    
        elif DATATYPE.data_type_all_by_finished == data_type:
            try:
                finished = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: finished parameters is required for data_type_all_byfinished"
                raise InvalidKeyException("hot_media_handler", "finished")
            try:
                ret = self.session.query(hot_media).filter(hot_media.finished==finished).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_all_by_finished"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(hot_media).count()
                return ret
            except NoResultFound, e:
                print "hot_media_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "hot_media donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import hot_media
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "hot_media_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("hot_media_handler", "id")
            try:
                self.session.query(hot_media).filter(hot_media.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "hot_media_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class oss_operation_history_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(oss_operation_history_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import oss_operation_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_operation_history_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_operation_history).filter(oss_operation_history.id==id).all()
                else:
                    q = self.session.query(oss_operation_history).filter(oss_operation_history.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_operation_history_handler", "resource_type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_operation_history).filter(oss_operation_history.resource_type==resource_type).all()
                else:
                    q = self.session.query(oss_operation_history).filter(oss_operation_history.resource_type==resource_type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_operation_history_handler", "resource_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_operation_history).filter(oss_operation_history.resource_id==resource_id).all()
                else:
                    q = self.session.query(oss_operation_history).filter(oss_operation_history.resource_id==resource_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_username == data_type:
            try:
                username = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_operation_history_handler", "username")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_operation_history).filter(oss_operation_history.username==username).all()
                else:
                    q = self.session.query(oss_operation_history).filter(oss_operation_history.username==username)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_username"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(oss_operation_history).all()
                else:
                    q = self.session.query(oss_operation_history)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_operation_history donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import oss_operation_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("oss_operation_history_handler", "id")
            try:
                self.session.query(oss_operation_history).filter(oss_operation_history.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "oss_operation_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import oss_operation_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = oss_operation_history(**self.data_desc.modifier)
            except:
                print "fail to initialize the oss_operation_history instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "oss_operation_history process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "oss_operation_history process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import oss_operation_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_operation_history_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("oss_operation_history_handler", "id")
            try:
                ret = self.session.query(oss_operation_history).filter(oss_operation_history.id==id).count()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                print "oss_operation_history_handler: resource_type parameters is required for data_type_all_byresource_type"
                raise InvalidKeyException("oss_operation_history_handler", "resource_type")
            try:
                ret = self.session.query(oss_operation_history).filter(oss_operation_history.resource_type==resource_type).count()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                print "oss_operation_history_handler: resource_id parameters is required for data_type_all_byresource_id"
                raise InvalidKeyException("oss_operation_history_handler", "resource_id")
            try:
                ret = self.session.query(oss_operation_history).filter(oss_operation_history.resource_id==resource_id).count()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_username == data_type:
            try:
                username = self.data_desc.getKey(1)
            except:
                print "oss_operation_history_handler: username parameters is required for data_type_all_byusername"
                raise InvalidKeyException("oss_operation_history_handler", "username")
            try:
                ret = self.session.query(oss_operation_history).filter(oss_operation_history.username==username).count()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_all_by_username"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(oss_operation_history).count()
                return ret
            except NoResultFound, e:
                print "oss_operation_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "oss_operation_history donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import oss_operation_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "oss_operation_history_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("oss_operation_history_handler", "id")
            try:
                self.session.query(oss_operation_history).filter(oss_operation_history.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "oss_operation_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class resource_site_status_rel_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(resource_site_status_rel_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import resource_site_status_rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.id==id).all()
                else:
                    q = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "resource_type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_type==resource_type).all()
                else:
                    q = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_type==resource_type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "resource_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_id==resource_id).all()
                else:
                    q = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_id==resource_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_site_id == data_type:
            try:
                site_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "site_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.site_id==site_id).all()
                else:
                    q = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.site_id==site_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_site_id"
                raise e
    
        elif DATATYPE.data_type_all_by_online == data_type:
            try:
                online = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "online")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.online==online).all()
                else:
                    q = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.online==online)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_online"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(resource_site_status_rel).all()
                else:
                    q = self.session.query(resource_site_status_rel)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "resource_site_status_rel donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import resource_site_status_rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("resource_site_status_rel_handler", "id")
            try:
                self.session.query(resource_site_status_rel).filter(resource_site_status_rel.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import resource_site_status_rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = resource_site_status_rel(**self.data_desc.modifier)
            except:
                print "fail to initialize the resource_site_status_rel instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "resource_site_status_rel process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "resource_site_status_rel process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import resource_site_status_rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("resource_site_status_rel_handler", "id")
            try:
                ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.id==id).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: resource_type parameters is required for data_type_all_byresource_type"
                raise InvalidKeyException("resource_site_status_rel_handler", "resource_type")
            try:
                ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_type==resource_type).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: resource_id parameters is required for data_type_all_byresource_id"
                raise InvalidKeyException("resource_site_status_rel_handler", "resource_id")
            try:
                ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.resource_id==resource_id).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_site_id == data_type:
            try:
                site_id = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: site_id parameters is required for data_type_all_bysite_id"
                raise InvalidKeyException("resource_site_status_rel_handler", "site_id")
            try:
                ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.site_id==site_id).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_site_id"
                raise e
    
        elif DATATYPE.data_type_all_by_online == data_type:
            try:
                online = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: online parameters is required for data_type_all_byonline"
                raise InvalidKeyException("resource_site_status_rel_handler", "online")
            try:
                ret = self.session.query(resource_site_status_rel).filter(resource_site_status_rel.online==online).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_online"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(resource_site_status_rel).count()
                return ret
            except NoResultFound, e:
                print "resource_site_status_rel_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "resource_site_status_rel donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import resource_site_status_rel
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "resource_site_status_rel_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("resource_site_status_rel_handler", "id")
            try:
                self.session.query(resource_site_status_rel).filter(resource_site_status_rel.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "resource_site_status_rel_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class basic_liveshow_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_liveshow_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_liveshow
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.id==id).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_sourceId == data_type:
            try:
                sourceId = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "sourceId")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.sourceId==sourceId).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.sourceId==sourceId)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_sourceId"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "vender_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.vender_id==vender_id).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.vender_id==vender_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_escape_title == data_type:
            try:
                escape_title = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "escape_title")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.escape_title==escape_title).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.escape_title==escape_title)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_escape_title"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "is_sync")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.is_sync==is_sync).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.is_sync==is_sync)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_all_by_site_status == data_type:
            try:
                site_status = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "site_status")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).filter(basic_liveshow.site_status==site_status).all()
                else:
                    q = self.session.query(basic_liveshow).filter(basic_liveshow.site_status==site_status)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_site_status"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_liveshow).all()
                else:
                    q = self.session.query(basic_liveshow)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_liveshow donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_liveshow
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_liveshow_handler", "id")
            try:
                self.session.query(basic_liveshow).filter(basic_liveshow.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_liveshow_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_liveshow
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_liveshow(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_liveshow instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_liveshow process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_liveshow process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_liveshow
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_liveshow_handler", "id")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_sourceId == data_type:
            try:
                sourceId = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: sourceId parameters is required for data_type_all_bysourceId"
                raise InvalidKeyException("basic_liveshow_handler", "sourceId")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.sourceId==sourceId).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_sourceId"
                raise e
    
        elif DATATYPE.data_type_all_by_vender_id == data_type:
            try:
                vender_id = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: vender_id parameters is required for data_type_all_byvender_id"
                raise InvalidKeyException("basic_liveshow_handler", "vender_id")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.vender_id==vender_id).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_vender_id"
                raise e
    
        elif DATATYPE.data_type_all_by_escape_title == data_type:
            try:
                escape_title = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: escape_title parameters is required for data_type_all_byescape_title"
                raise InvalidKeyException("basic_liveshow_handler", "escape_title")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.escape_title==escape_title).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_escape_title"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: is_sync parameters is required for data_type_all_byis_sync"
                raise InvalidKeyException("basic_liveshow_handler", "is_sync")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.is_sync==is_sync).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_all_by_site_status == data_type:
            try:
                site_status = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: site_status parameters is required for data_type_all_bysite_status"
                raise InvalidKeyException("basic_liveshow_handler", "site_status")
            try:
                ret = self.session.query(basic_liveshow).filter(basic_liveshow.site_status==site_status).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_all_by_site_status"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_liveshow).count()
                return ret
            except NoResultFound, e:
                print "basic_liveshow_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_liveshow donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_liveshow
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_liveshow_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_liveshow_handler", "id")
            try:
                self.session.query(basic_liveshow).filter(basic_liveshow.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_liveshow_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class basic_entertainer_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(basic_entertainer_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import basic_entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_entertainer_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_entertainer).filter(basic_entertainer.id==id).all()
                else:
                    q = self.session.query(basic_entertainer).filter(basic_entertainer.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_stagename == data_type:
            try:
                stagename = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_entertainer_handler", "stagename")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_entertainer).filter(basic_entertainer.stagename==stagename).all()
                else:
                    q = self.session.query(basic_entertainer).filter(basic_entertainer.stagename==stagename)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_stagename"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_entertainer_handler", "is_sync")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_entertainer).filter(basic_entertainer.is_sync==is_sync).all()
                else:
                    q = self.session.query(basic_entertainer).filter(basic_entertainer.is_sync==is_sync)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(basic_entertainer).all()
                else:
                    q = self.session.query(basic_entertainer)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_entertainer donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import basic_entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("basic_entertainer_handler", "id")
            try:
                self.session.query(basic_entertainer).filter(basic_entertainer.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "basic_entertainer_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import basic_entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = basic_entertainer(**self.data_desc.modifier)
            except:
                print "fail to initialize the basic_entertainer instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "basic_entertainer process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "basic_entertainer process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import basic_entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_entertainer_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("basic_entertainer_handler", "id")
            try:
                ret = self.session.query(basic_entertainer).filter(basic_entertainer.id==id).count()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_stagename == data_type:
            try:
                stagename = self.data_desc.getKey(1)
            except:
                print "basic_entertainer_handler: stagename parameters is required for data_type_all_bystagename"
                raise InvalidKeyException("basic_entertainer_handler", "stagename")
            try:
                ret = self.session.query(basic_entertainer).filter(basic_entertainer.stagename==stagename).count()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_stagename"
                raise e
    
        elif DATATYPE.data_type_all_by_is_sync == data_type:
            try:
                is_sync = self.data_desc.getKey(1)
            except:
                print "basic_entertainer_handler: is_sync parameters is required for data_type_all_byis_sync"
                raise InvalidKeyException("basic_entertainer_handler", "is_sync")
            try:
                ret = self.session.query(basic_entertainer).filter(basic_entertainer.is_sync==is_sync).count()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_all_by_is_sync"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(basic_entertainer).count()
                return ret
            except NoResultFound, e:
                print "basic_entertainer_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "basic_entertainer donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import basic_entertainer
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "basic_entertainer_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("basic_entertainer_handler", "id")
            try:
                self.session.query(basic_entertainer).filter(basic_entertainer.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "basic_entertainer_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
class update_history_handler(db_handler):
    def __init__(self, op, data_desc, session=None):
        super(update_history_handler, self).__init__(op, data_desc, session)
        
    def processQuery(self):
        from ..datamodel.schema import update_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.id==id).all()
                else:
                    q = self.session.query(update_history).filter(update_history.id==id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "resource_type")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.resource_type==resource_type).all()
                else:
                    q = self.session.query(update_history).filter(update_history.resource_type==resource_type)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "resource_id")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.resource_id==resource_id).all()
                else:
                    q = self.session.query(update_history).filter(update_history.resource_id==resource_id)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_title == data_type:
            try:
                resource_title = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "resource_title")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.resource_title==resource_title).all()
                else:
                    q = self.session.query(update_history).filter(update_history.resource_title==resource_title)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_title"
                raise e
    
        elif DATATYPE.data_type_all_by_auto == data_type:
            try:
                auto = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "auto")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.auto==auto).all()
                else:
                    q = self.session.query(update_history).filter(update_history.auto==auto)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_auto"
                raise e
    
        elif DATATYPE.data_type_all_by_action == data_type:
            try:
                action = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "action")
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).filter(update_history.action==action).all()
                else:
                    q = self.session.query(update_history).filter(update_history.action==action)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_action"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            start, amount = self.data_desc.getPageInfo()
            try:
                ret = None
                if amount == 0:
                    ret = self.session.query(update_history).all()
                else:
                    q = self.session.query(update_history)
                    ret = slice_query(q, start, amount).all()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "update_history donot support DataType ", data_type
            raise NoSupportDataType
       
    def processUpdate(self):
        from ..datamodel.schema import update_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_update_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                raise InvalidKeyException("update_history_handler", "id")
            try:
                self.session.query(update_history).filter(update_history.id==id).update(self.data_desc.modifier)
                self.session.commit()
            except NoResultFound:
                print "update_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
    def processInsert(self):
        from ..datamodel.schema import update_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_insert_record == data_type:
            try:
                t = update_history(**self.data_desc.modifier)
            except:
                print "fail to initialize the update_history instance, check the modifier %s"%self.data_desc.modifier
                return None
            try:
                self.session.add(t)
                self.session.commit()
            except:
                print "update_history process insert fail for %s"%self.data_desc.modifier
                return None
            return t
        else:
            print "update_history process insert donot support DataType ", data_type
            return None
       
    def processCount(self):
        from ..datamodel.schema import update_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_all_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "update_history_handler: id parameters is required for data_type_all_byid"
                raise InvalidKeyException("update_history_handler", "id")
            try:
                ret = self.session.query(update_history).filter(update_history.id==id).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_type == data_type:
            try:
                resource_type = self.data_desc.getKey(1)
            except:
                print "update_history_handler: resource_type parameters is required for data_type_all_byresource_type"
                raise InvalidKeyException("update_history_handler", "resource_type")
            try:
                ret = self.session.query(update_history).filter(update_history.resource_type==resource_type).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_type"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_id == data_type:
            try:
                resource_id = self.data_desc.getKey(1)
            except:
                print "update_history_handler: resource_id parameters is required for data_type_all_byresource_id"
                raise InvalidKeyException("update_history_handler", "resource_id")
            try:
                ret = self.session.query(update_history).filter(update_history.resource_id==resource_id).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_id"
                raise e
    
        elif DATATYPE.data_type_all_by_resource_title == data_type:
            try:
                resource_title = self.data_desc.getKey(1)
            except:
                print "update_history_handler: resource_title parameters is required for data_type_all_byresource_title"
                raise InvalidKeyException("update_history_handler", "resource_title")
            try:
                ret = self.session.query(update_history).filter(update_history.resource_title==resource_title).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_resource_title"
                raise e
    
        elif DATATYPE.data_type_all_by_auto == data_type:
            try:
                auto = self.data_desc.getKey(1)
            except:
                print "update_history_handler: auto parameters is required for data_type_all_byauto"
                raise InvalidKeyException("update_history_handler", "auto")
            try:
                ret = self.session.query(update_history).filter(update_history.auto==auto).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_auto"
                raise e
    
        elif DATATYPE.data_type_all_by_action == data_type:
            try:
                action = self.data_desc.getKey(1)
            except:
                print "update_history_handler: action parameters is required for data_type_all_byaction"
                raise InvalidKeyException("update_history_handler", "action")
            try:
                ret = self.session.query(update_history).filter(update_history.action==action).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_all_by_action"
                raise e
    
        elif DATATYPE.data_type_query_all == data_type:
            try:
                ret = self.session.query(update_history).count()
                return ret
            except NoResultFound, e:
                print "update_history_handler: no record found for data_type_query_all"
                raise e
    
        else:
            print "update_history donot support DataType ", data_type
            raise NoSupportDataType           
       
    def processDelete(self):
        from ..datamodel.schema import update_history
        data_type = self.data_desc.getDataType()
    
        if DATATYPE.data_type_del_by_id == data_type:
            try:
                id = self.data_desc.getKey(1)
            except:
                print "update_history_handler: id parameters is required for data_type_del_by_id"
                raise InvalidKeyException("update_history_handler", "id")
            try:
                self.session.query(update_history).filter(update_history.id==id).delete()
                self.session.commit()
            except NoResultFound:
                print "update_history_handler: no record found for data_type_all_by_id for id (%s)"%id
        else:
            print "update operation donot support DataType ", data_type
            raise NoSupportDataType
       
def default_db_get(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_basic_vender == schema:
        handler = basic_vender_handler("get", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("get", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("get", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("get", data_desc)
    elif SCHEMA.schema_basic_category == schema:
        handler = basic_category_handler("get", data_desc)
    elif SCHEMA.schema_basic_media == schema:
        handler = basic_media_handler("get", data_desc)
    elif SCHEMA.schema_basic_program == schema:
        handler = basic_program_handler("get", data_desc)
    elif SCHEMA.schema_audit == schema:
        handler = audit_handler("get", data_desc)
    elif SCHEMA.schema_site_system == schema:
        handler = site_system_handler("get", data_desc)
    elif SCHEMA.schema_rule_vender == schema:
        handler = rule_vender_handler("get", data_desc)
    elif SCHEMA.schema_rule_media == schema:
        handler = rule_media_handler("get", data_desc)
    elif SCHEMA.schema_import_history == schema:
        handler = import_history_handler("get", data_desc)
    elif SCHEMA.schema_hot_media == schema:
        handler = hot_media_handler("get", data_desc)
    elif SCHEMA.schema_oss_operation_history == schema:
        handler = oss_operation_history_handler("get", data_desc)
    elif SCHEMA.schema_resource_site_status_rel == schema:
        handler = resource_site_status_rel_handler("get", data_desc)
    elif SCHEMA.schema_basic_liveshow == schema:
        handler = basic_liveshow_handler("get", data_desc)
    elif SCHEMA.schema_basic_entertainer == schema:
        handler = basic_entertainer_handler("get", data_desc)
    elif SCHEMA.schema_update_history == schema:
        handler = update_history_handler("get", data_desc)
    
    else:
        print "default_db_get donot support schema ", schema
        return None
    return handler
    
def default_db_update(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_basic_vender == schema:
        handler = basic_vender_handler("upd", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("upd", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("upd", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("upd", data_desc)
    elif SCHEMA.schema_basic_category == schema:
        handler = basic_category_handler("upd", data_desc)
    elif SCHEMA.schema_basic_media == schema:
        handler = basic_media_handler("upd", data_desc)
    elif SCHEMA.schema_basic_program == schema:
        handler = basic_program_handler("upd", data_desc)
    elif SCHEMA.schema_audit == schema:
        handler = audit_handler("upd", data_desc)
    elif SCHEMA.schema_site_system == schema:
        handler = site_system_handler("upd", data_desc)
    elif SCHEMA.schema_rule_vender == schema:
        handler = rule_vender_handler("upd", data_desc)
    elif SCHEMA.schema_rule_media == schema:
        handler = rule_media_handler("upd", data_desc)
    elif SCHEMA.schema_import_history == schema:
        handler = import_history_handler("upd", data_desc)
    elif SCHEMA.schema_hot_media == schema:
        handler = hot_media_handler("upd", data_desc)
    elif SCHEMA.schema_oss_operation_history == schema:
        handler = oss_operation_history_handler("upd", data_desc)
    elif SCHEMA.schema_resource_site_status_rel == schema:
        handler = resource_site_status_rel_handler("upd", data_desc)
    elif SCHEMA.schema_basic_liveshow == schema:
        handler = basic_liveshow_handler("upd", data_desc)
    elif SCHEMA.schema_basic_entertainer == schema:
        handler = basic_entertainer_handler("upd", data_desc)
    elif SCHEMA.schema_update_history == schema:
        handler = update_history_handler("upd", data_desc)
    
    else:
        print "default_db_update donot support schema ", schema
        return None
    return handler
    
def default_db_insert(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_basic_vender == schema:
        handler = basic_vender_handler("insr", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("insr", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("insr", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("insr", data_desc)
    elif SCHEMA.schema_basic_category == schema:
        handler = basic_category_handler("insr", data_desc)
    elif SCHEMA.schema_basic_media == schema:
        handler = basic_media_handler("insr", data_desc)
    elif SCHEMA.schema_basic_program == schema:
        handler = basic_program_handler("insr", data_desc)
    elif SCHEMA.schema_audit == schema:
        handler = audit_handler("insr", data_desc)
    elif SCHEMA.schema_site_system == schema:
        handler = site_system_handler("insr", data_desc)
    elif SCHEMA.schema_rule_vender == schema:
        handler = rule_vender_handler("insr", data_desc)
    elif SCHEMA.schema_rule_media == schema:
        handler = rule_media_handler("insr", data_desc)
    elif SCHEMA.schema_import_history == schema:
        handler = import_history_handler("insr", data_desc)
    elif SCHEMA.schema_hot_media == schema:
        handler = hot_media_handler("insr", data_desc)
    elif SCHEMA.schema_oss_operation_history == schema:
        handler = oss_operation_history_handler("insr", data_desc)
    elif SCHEMA.schema_resource_site_status_rel == schema:
        handler = resource_site_status_rel_handler("insr", data_desc)
    elif SCHEMA.schema_basic_liveshow == schema:
        handler = basic_liveshow_handler("insr", data_desc)
    elif SCHEMA.schema_basic_entertainer == schema:
        handler = basic_entertainer_handler("insr", data_desc)
    elif SCHEMA.schema_update_history == schema:
        handler = update_history_handler("insr", data_desc)
    
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    
def default_db_count(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_basic_vender == schema:
        handler = basic_vender_handler("count", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("count", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("count", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("count", data_desc)
    elif SCHEMA.schema_basic_category == schema:
        handler = basic_category_handler("count", data_desc)
    elif SCHEMA.schema_basic_media == schema:
        handler = basic_media_handler("count", data_desc)
    elif SCHEMA.schema_basic_program == schema:
        handler = basic_program_handler("count", data_desc)
    elif SCHEMA.schema_audit == schema:
        handler = audit_handler("count", data_desc)
    elif SCHEMA.schema_site_system == schema:
        handler = site_system_handler("count", data_desc)
    elif SCHEMA.schema_rule_vender == schema:
        handler = rule_vender_handler("count", data_desc)
    elif SCHEMA.schema_rule_media == schema:
        handler = rule_media_handler("count", data_desc)
    elif SCHEMA.schema_import_history == schema:
        handler = import_history_handler("count", data_desc)
    elif SCHEMA.schema_hot_media == schema:
        handler = hot_media_handler("count", data_desc)
    elif SCHEMA.schema_oss_operation_history == schema:
        handler = oss_operation_history_handler("count", data_desc)
    elif SCHEMA.schema_resource_site_status_rel == schema:
        handler = resource_site_status_rel_handler("count", data_desc)
    elif SCHEMA.schema_basic_liveshow == schema:
        handler = basic_liveshow_handler("count", data_desc)
    elif SCHEMA.schema_basic_entertainer == schema:
        handler = basic_entertainer_handler("count", data_desc)
    elif SCHEMA.schema_update_history == schema:
        handler = update_history_handler("count", data_desc)
    
    else:
        print "default_db_count donot support schema ", schema
        return None
    return handler
    
def default_db_delete(data_desc, session):
    schema = data_desc.getSchema()
    dat_type = data_desc.getSchema()
    handler = None
    if SCHEMA.schema_basic_vender == schema:
        handler = basic_vender_handler("del", data_desc)
    elif SCHEMA.schema_vender_attr_mapping == schema:
        handler = vender_attr_mapping_handler("del", data_desc)
    elif SCHEMA.schema_oss_user == schema:
        handler = oss_user_handler("del", data_desc)
    elif SCHEMA.schema_medias_update_record == schema:
        handler = medias_update_record_handler("del", data_desc)
    elif SCHEMA.schema_basic_category == schema:
        handler = basic_category_handler("del", data_desc)
    elif SCHEMA.schema_basic_media == schema:
        handler = basic_media_handler("del", data_desc)
    elif SCHEMA.schema_basic_program == schema:
        handler = basic_program_handler("del", data_desc)
    elif SCHEMA.schema_audit == schema:
        handler = audit_handler("del", data_desc)
    elif SCHEMA.schema_site_system == schema:
        handler = site_system_handler("del", data_desc)
    elif SCHEMA.schema_rule_vender == schema:
        handler = rule_vender_handler("del", data_desc)
    elif SCHEMA.schema_rule_media == schema:
        handler = rule_media_handler("del", data_desc)
    elif SCHEMA.schema_import_history == schema:
        handler = import_history_handler("del", data_desc)
    elif SCHEMA.schema_hot_media == schema:
        handler = hot_media_handler("del", data_desc)
    elif SCHEMA.schema_oss_operation_history == schema:
        handler = oss_operation_history_handler("del", data_desc)
    elif SCHEMA.schema_resource_site_status_rel == schema:
        handler = resource_site_status_rel_handler("del", data_desc)
    elif SCHEMA.schema_basic_liveshow == schema:
        handler = basic_liveshow_handler("del", data_desc)
    elif SCHEMA.schema_basic_entertainer == schema:
        handler = basic_entertainer_handler("del", data_desc)
    elif SCHEMA.schema_update_history == schema:
        handler = update_history_handler("del", data_desc)
    
    else:
        print "default_db_insert donot support schema ", schema
        return None
    return handler
    