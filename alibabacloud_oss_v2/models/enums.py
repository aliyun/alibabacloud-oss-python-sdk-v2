"""Enum for operation APIs"""
from enum import Enum


class BucketACLType(str, Enum):
    """
    The access control list (ACL) of the bucket.
    """

    PRIVATE = 'private'
    """
    Only the bucket owner can perform read and write operations on objects in the bucket.
    Other users cannot access the objects in the bucket.
    """

    PUBLICREAD = 'public-read'
    """
    Only the bucket owner can write data to objects in the bucket.
    Other users, including anonymous users, can only read objects in the bucket.
    """

    PUBLICREADWRITE = 'public-read-write'
    """
    All users, including anonymous users, can perform read and write operations on the bucket.
    """


class StorageClassType(str, Enum):
    """
    The storage class of the bucket.
    """

    STANDARD = 'Standard'
    """
    Standard provides highly reliable, highly available and high-performance object storage
    for data that is frequently accessed.    
    """

    IA = 'IA'
    """
    IA provides highly durable storage at lower prices compared with Standard.
	It has a minimum billable size of 64 KB and a minimum billable storage duration of 30 days.    
    """

    ARCHIVE = 'Archive'
    """
    Archive provides high-durability storage at lower prices compared with Standard and IA.
	It has a minimum billable size of 64 KB and a minimum billable storage duration of 60 days.
    """

    COLDARCHIVE = 'ColdArchive'
    """
    Cold Archive provides highly durable storage at lower prices compared with Archive.
	It has a minimum billable size of 64 KB and a minimum billable storage duration of 180 days.    
    """

    DEEPCOLDARCHIVE = 'DeepColdArchive'
    """
    Deep Cold Archive provides highly durable storage at lower prices compared with Cold Archive.
	It has a minimum billable size of 64 KB and a minimum billable storage duration of 180 days.    
    """


class DataRedundancyType(str, Enum):
    """
    The redundancy type of the bucket.
    """

    LRS = 'LRS'
    """
    LRS Locally redundant storage(LRS) stores copies of each object across different devices 
    in the same zone. This ensures data reliability and availability even if two storage devices
    are damaged at the same time.
    """

    ZRS = 'ZRS'
    """
    ZRS Zone-redundant storage(ZRS) uses the multi-zone mechanism to distribute user data across
    multiple zones in the same region. If one zone becomes unavailable, you can continue to 
    access the data that is stored in other zones.
    """


class ObjectACLType(str, Enum):
    """
    The access control list(ACL) of the object.
    """

    PRIVATE = 'private'
    """
    Only the object owner is allowed to perform read and write operations on the object.
    Other users cannot access the object.
    """

    PUBLICREAD = 'public-read'
    """
    Only the object owner can write data to the object.
    Other users, including anonymous users, can only read the object.
    """

    PUBLICREADWRITE = 'public-read-write'
    """
    All users, including anonymous users, can perform read and write operations on the object.
    """

    DEFAULT = 'default'
    """
    The ACL of the object is the same as that of the bucket in which the object is stored.
    """
