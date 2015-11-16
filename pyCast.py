#!/usr/bin/env python

from __future__ import print_function
import os, sys, getopt, mimetypes, datetime, urllib
import  xml.etree.cElementTree as ET

from Foundation import *


attrKeys = { 'kMDItemAlbum': 'Album', 'kMDItemDurationSeconds': 'Duration', 'kMDItemDisplayName': 'Title', 'kMDItemContentCreationDate': 'PubDate', 
            'kMDItemLogicalSize': 'Size', 'kMDItemComment': 'Summary', 'kMDItemAuthors': 'Authors' }

def getMeta( fileName ):
    fileDets = {}
    if os.path.exists( fileName ):
        mdRef = NSURL.fileURLWithPath_( fileName )
        mdItem = NSMetadataItem.alloc().initWithURL_( mdRef )
        for indivKey in attrKeys.keys():
            fileDets[ attrKeys[ indivKey ] ] = mdItem.valueForAttribute_( indivKey )
            
    return fileDets

def genFeed( srcDir ):
    for fileFound in os.listdir( srcDir ):
        if fileFound.startswith( '.' ):
            continue
        yield fileFound

def main( argv = None ):
    if argv is None:
        argv = sys.argv
        
    optList, optArgs = getopt.getopt( argv[ 1: ], "w:d:h", [ '--web', '--dir', '--help' ] )
    webBase = None
    dirBase = None
    for clList, clArgs in optList:
        if clList in [ '-w', '--web' ]:
            webBase = clArgs
        elif clList in [ '-d', '--dir' ]:
            dirBase = clArgs

    if dirBase is None:
        print( 'Base Dir Not Specified!' )
        return 1
                    
    for srcDir in os.listdir( dirBase ):
        if os.path.isfile( os.path.join( dirBase, srcDir ) ):
            continue
                        
        rssRoot = ET.Element( "rss" )
        rssChann = ET.SubElement( rssRoot, 'channel' )
        rssChann.attrib[ 'xmlns:itunes' ] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        rssChann.attrib[ 'version' ] = '2.0'
        
        castTitle = ET.SubElement( rssChann, 'title' )
        castLink = ET.SubElement( rssChann, 'link' )
        castDesc = ET.SubElement( rssChann, 'description' )
        castiTunesDesc = ET.SubElement( rssChann, 'itunes:summary' )
        castiTunesArtist = ET.SubElement( rssChann, 'itunes:author' )
        
        fullPath = os.path.join( dirBase, srcDir )
        for fileName in genFeed( fullPath ):
            relPath = os.path.join( srcDir, fileName ) 
            fullURL = os.path.join( webBase, urllib.quote( relPath ) )
            metaInfo = getMeta( os.path.join( fullPath, fileName ) )
            if metaInfo[ 'Title' ] == '':
                metaInfo[ 'Title' ] = srcDir
             
            castTitle.text = metaInfo[ 'Album' ] 
            castLink.text = webBase
            castDesc.text = metaInfo[ 'Summary' ]
            castiTunesDesc.text = metaInfo[ 'Summary' ]
            castiTunesArtist.text = str( metaInfo[ 'Authors' ] )
            
            castItem = ET.SubElement( rssChann, 'item' )
            
            itemTitle = ET.SubElement( castItem, 'title' )
            itemTitle.text = metaInfo[ 'Title' ]
            
            itemEnc = ET.SubElement( castItem, 'enclosure' )
            itemEnc.attrib[ 'url' ] = str( fullURL )
            itemEnc.attrib[ 'length' ] = str( metaInfo[ 'Size' ] )
            mimeType = mimetypes.guess_type( fullURL )[ 0 ]
            if not mimeType is None:
                itemEnc.attrib[ 'type' ] =  mimetypes.guess_type( fullURL )[ 0 ]
            else:
                if fileName.endswith( 'm4b' ):
                    itemEnc.attrib[ 'type' ] = 'audio/x-m4b'
            
            itemPubDate = ET.SubElement( castItem, 'pubDate' )
            itemPubDate.text = str( metaInfo[ 'PubDate' ] )
            
            itemGUID = ET.SubElement( castItem, 'guid' )
            itemGUID.text = fullURL
            
            itemiTunesAuthor = ET.SubElement( castItem, 'itunes:author' )
            itemiTunesAuthor.text = str( metaInfo[ 'Authors' ] )
            
            itemiTunesSummary = ET.SubElement( castItem, 'itunes:summary' )
            itemiTunesSummary.text = str( metaInfo[ 'Summary' ] )
            
            itemiTunesSubtitle = ET.SubElement( castItem, 'itunes:subtitle' )
            itemiTunesSubtitle.text = str( metaInfo[ 'Summary' ] )

            itemiTunesDuration = ET.SubElement( castItem, 'itunes:duration' )
            stringDuration = str( datetime.timedelta( seconds=int( metaInfo[ 'Duration' ] ) ) )
            itemiTunesDuration.text = stringDuration
            
        fullXML = ET.ElementTree( rssRoot )
        ET.dump( fullXML )
        xmlPath = os.path.join( dirBase, '%s.xml' % srcDir )
        fullXML.write ( xmlPath  )            

if __name__ == '__main__':
    sys.exit( main() )
    
    
    
    
