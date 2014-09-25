<?xml version="1.0" ?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/"
	xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

 <xsl:output encoding="UTF-8" indent="no"/>

 <!--Main Template-->
 <xsl:template match="/">
	<xsl:element name="rdf:RDF">
		<xsl:for-each select="//response/result/doc">
			<xsl:call-template name="document"/>
		</xsl:for-each>
	</xsl:element>
 </xsl:template>

 <!-- process each record -->
 <xsl:template name="document">
	<xsl:element name="rdf:Description">
		<xsl:attribute name="rdf:about">
			<xsl:value-of select="str[@name='url']" />
		</xsl:attribute>
		<xsl:element name="dc:identifier">
			<xsl:value-of select="str[@name='url']" />
		</xsl:element>
 		<dc:title>
 			<xsl:value-of select="./arr[@name='title']"/>
 		</dc:title>
		<xsl:if test="string-length(arr[@name='creator']) &gt; 0">
			<dc:creator>
				<xsl:value-of select="./arr[@name='creator']"/>
			</dc:creator>
		</xsl:if>
		<xsl:if test="string-length(arr[@name='contributor']) &gt; 0">
			<dc:contributor>
				<xsl:value-of select="./arr[@name='contributor']"/>
			</dc:contributor>
		</xsl:if>
		<xsl:if test="string-length(arr[@name='publisher']) &gt; 0">
			<dc:publisher>
				<xsl:value-of select="./arr[@name='publisher']"/>
			</dc:publisher>
		</xsl:if>
		<xsl:if test="string-length(arr[@name='source']) &gt; 0">
			<dc:source>
				<xsl:value-of select="./arr[@name='source']"/>
			</dc:source>
		</xsl:if>
		<xsl:if test="string-length(arr[@name='bibliographicCitation']) &gt; 0">
			<dcterms:bibliographicCitation>
				<xsl:value-of select="./arr[@name='bibliographicCitation']"/>
			</dcterms:bibliographicCitation>
		</xsl:if>
		<xsl:if test="string-length(arr[@name='temporal']) &gt; 0">
			<dcterms:temporal>
				<xsl:value-of select="./arr[@name='temporal']"/>
			</dcterms:temporal>
		</xsl:if>
		<dc:description>
			<xsl:value-of select="./arr[@name='description']"/><xsl:text> </xsl:text>
		</dc:description>

		<xsl:if test="string-length(arr[@name='subject']) &gt; 0">
			<xsl:for-each select="arr[@name='subject']/str">
				<dc:subject>
					<xsl:value-of select="."/>
				</dc:subject>
			</xsl:for-each>
		</xsl:if>

		<xsl:element name="dcterms:issued">
			<xsl:value-of select="date[@name='madePublic']" />
		</xsl:element>
		<xsl:element name="dcterms:modified">
			<xsl:value-of select="date[@name='modified']" />
		</xsl:element>
		<xsl:element name="dc:type">
			<xsl:choose>
				<xsl:when test="arr[@name='mediaType'] = 'image'">StillImage</xsl:when>
				<xsl:when test="arr[@name='mediaType'] = 'video'">MovingImage</xsl:when>
				<xsl:otherwise><xsl:value-of select="arr[@name='mediaType']" /></xsl:otherwise>
			</xsl:choose>
		</xsl:element>
		<xsl:if test="string-length(arr[@name='spatial']) &gt; 0">
			<dcterms:spatial>
				<xsl:value-of select="./arr[@name='spatial']"/>
			</dcterms:spatial>
		</xsl:if>
		<xsl:if test="string-length(float[@name='itemLatitude']) &gt; 0">
			<!--<geo:Point>-->
				<geo:lat><xsl:value-of select="float[@name='itemLatitude']" /></geo:lat>
				<geo:long><xsl:value-of select="float[@name='itemLongitude']" /></geo:long>
			<!--</geo:Point>-->
		</xsl:if>
		<xsl:if test="string-length(arr[@name='language']) &gt; 0">
			<dc:language>
				<xsl:value-of select="./arr[@name='language']"/>
			</dc:language>
		</xsl:if>
	</xsl:element>
 </xsl:template>


</xsl:stylesheet>

