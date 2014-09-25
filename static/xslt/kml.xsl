<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/"
	xmlns:georss="http://www.georss.org/georss">

	<xsl:output method="xml"/>
	<xsl:template match="/">
		<kml xmlns="http://earth.google.com/kml/2.1">
			<Document>
			<xsl:call-template name="kml" />
			</Document>
		</kml>
	</xsl:template>


 <xsl:template name="kml">
	<xsl:for-each select="//doc">
		<xsl:if test="string-length(./float[@name='itemLatitude']) &gt; 0">
		<Placemark>
			<name><xsl:value-of select="./arr[@name='title']"/></name>
			<title>
				<xsl:value-of select="./arr[@name='title']"/>
			</title>
			<description>
				<xsl:text>&lt;p&gt;&lt;a href=&quot;</xsl:text>
				<xsl:value-of select="./str[@name='url']"/>
				<xsl:text>&quot;&gt;&lt;img src=&quot;</xsl:text>
				<xsl:value-of select="./str[@name='thumbnail']"/>
				<xsl:text>&quot; alt=&quot;</xsl:text>
				<xsl:value-of select="./arr[@name='title']"/>
				<xsl:text>&quot; /&gt;&lt;/a&gt;&lt;/p&gt;</xsl:text>

				<xsl:text>&lt;p&gt;</xsl:text>
				<xsl:value-of select="./arr[@name='description']"/>
				<xsl:text>&lt;/p&gt;</xsl:text>
			</description>
			<Point>
				<coordinates>
				<xsl:value-of select="float[@name='itemLongitude']" />
				<xsl:text>,</xsl:text>
				<xsl:value-of select="float[@name='itemLatitude']" />
				</coordinates>
			</Point>
		</Placemark>
		</xsl:if>
	</xsl:for-each>
 </xsl:template>

</xsl:stylesheet>
