<?xml version="1.0" ?>
<xsl:stylesheet 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:georss="http://www.georss.org/georss"
	xmlns:media="http://search.yahoo.com/mrss/"
	xmlns:atom="http://www.w3.org/2005/Atom">

 
<xsl:param name="pageName">RSS</xsl:param>
<xsl:param name="langLink">rss</xsl:param>
<xsl:param name="serverURL">http://search.ourontario.ca/</xsl:param>

 <xsl:output encoding="UTF-8" indent="no" method="xml" omit-xml-declaration="no" />

 <!--Main Template-->

 <xsl:template match="/">
	
<rss version="2.0" xmlns:georss="http://www.georss.org/georss" xmlns:atom="http://www.w3.org/2005/Atom">
	<channel>
	<title>OurOntario.ca Search</title>
	<link><xsl:value-of select="$serverURL"/>search</link>
	<description>One stop access to digital collections of libraries, archives, museums, historical societies, community groups, government agencies, and private collections in Ontario and across Canada.</description>
	<language>en-ca</language>
	<pubDate>2011-11-14T00:00:00Z</pubDate>
	<lastBuildDate>2011-11-14T00:00:00Z</lastBuildDate>
	<docs>http://blogs.law.harvard.edu/tech/rss</docs>
	<image>
		<url><xsl:value-of select="$serverURL"/>rsstile_88x31.gif</url>
		<title>OurOntario.ca Search</title>
		<link><xsl:value-of select="$serverURL"/>search</link>
		<width>88</width>
		<height>31</height>
	</image>
	<atom:icon>rsstile_88x31.gif</atom:icon>
		<xsl:call-template name="paging" />
	
		<xsl:element name="atom:link">
			<xsl:attribute name="rel">self</xsl:attribute>
			<xsl:attribute name="type">application/rss+xml</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:value-of select="$serverURL"/><xsl:text>rss?</xsl:text><xsl:value-of select="translate(//unparsedQuery,' ','+')"/>
			</xsl:attribute>
		</xsl:element>
		<xsl:for-each select="//response/result/doc">
			<xsl:call-template name="document"/>
		</xsl:for-each>
	</channel>
</rss>
 </xsl:template>

 <!-- process each record -->
 <xsl:template name="document">
 	<item>
 		<title>
 			<xsl:value-of select="./arr[@name='title']"/>
 		</title>
		<xsl:call-template name="description"/>
		<xsl:element name="link">
			<xsl:value-of select="str[@name='url']" />
		</xsl:element>
		<xsl:if test="string-length(date[@name='madePublic']) > 0">
			<xsl:element name="pubDate">
				<xsl:value-of select="date[@name='madePublic']" />
			</xsl:element>
		</xsl:if>
		<xsl:element name="guid">
			<xsl:attribute name="isPermaLink">true</xsl:attribute>
			<xsl:value-of select="str[@name='url']" />
		</xsl:element>
		<xsl:if test="string-length(str[@name='thumbnail']) &gt; 0">
			<xsl:element name="enclosure">
				<xsl:attribute name="url">
					<xsl:choose>
						<xsl:when test="string-length(str[@name='enclosureURL']) &gt; 0">
							<xsl:value-of select="str[@name='enclosureURL']" />
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="str[@name='thumbnail']" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:choose>
				<xsl:when test="int[@name='enclosureLength']">
					<xsl:attribute name="length"><xsl:value-of select="int[@name='enclosureLength']" /></xsl:attribute>
				</xsl:when>
				<xsl:otherwise><xsl:attribute name="length">23000</xsl:attribute></xsl:otherwise>
				</xsl:choose>
				<xsl:choose>
				<xsl:when test="string-length(int[@name='enclosureType']) &gt; 0">
					<xsl:attribute name="type"><xsl:value-of select="int[@name='enclosureType']" /></xsl:attribute>
				</xsl:when>
				<xsl:otherwise><xsl:attribute name="type">image/jpg</xsl:attribute></xsl:otherwise>
				</xsl:choose>
			</xsl:element>
			<xsl:element name="media:title">
				<xsl:value-of select="./arr[@name='title']"/>
			</xsl:element>
			<xsl:element name="media:content">
				<xsl:attribute name="url">
					<xsl:choose>
						<xsl:when test="string-length(str[@name='enclosureURL']) &gt; 0">
							<xsl:value-of select="str[@name='enclosureURL']" />
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="str[@name='thumbnail']" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:if test="int[@name='enclosureLength']">
					<xsl:attribute name="fileSize"><xsl:value-of select="int[@name='enclosureLength']" /></xsl:attribute>
				</xsl:if>
				<xsl:if test="string-length(int[@name='enclosureType']) &gt; 0">
					<xsl:attribute name="type"><xsl:value-of select="int[@name='enclosureType']" /></xsl:attribute>
				</xsl:if>
			</xsl:element>
			<xsl:if test="str[@name='thumbnail']">
				<xsl:element name="media:thumbnail">
					<xsl:attribute name="url"><xsl:value-of select="str[@name='thumbnail']" /></xsl:attribute>
				</xsl:element>
			</xsl:if>
		</xsl:if>
		<xsl:if test="string-length(float[@name='itemLatitude']) &gt; 0">
			<georss:point>
				<xsl:value-of select="float[@name='itemLatitude']" />
				<xsl:text> </xsl:text>
				<xsl:value-of select="float[@name='itemLongitude']" />
			</georss:point>
		</xsl:if>
	</item>
 </xsl:template>

 <xsl:template name="description">
	 <xsl:variable name="mydescription">
                <xsl:variable name="maxlen">300</xsl:variable>
                <xsl:choose>
                <xsl:when test="string-length(./arr[@name='description']) &lt;= $maxlen">
                        <xsl:value-of select="./arr[@name='description']"/>
                </xsl:when>
                <xsl:when test="not(contains(./arr[@name='description'],' '))">
                        <xsl:value-of select="substring(./arr[@name='description'],0,$maxlen)"/>
                        <xsl:text>...</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                        <xsl:call-template name="substring-before-last">
                        <xsl:with-param name="input" select="substring(
                                ./arr[@name='description'],0,$maxlen)"/>
                        <xsl:with-param name="substr" select="' '"/>
                        </xsl:call-template>
                        <xsl:text>...</xsl:text>
                </xsl:otherwise>
                </xsl:choose>
        </xsl:variable>
	<description>
	<xsl:value-of select="$mydescription"/>
	</description>
	<media:description>
		<xsl:value-of select="$mydescription"/>
	</media:description>
 </xsl:template>

 <xsl:template name="substring-before-last">
	<xsl:param name="input"/>
	<xsl:param name="substr"/>
	<xsl:if test="$substr and contains($input, $substr)">
		<xsl:variable name="temp" select="substring-after($input, $substr)"/>
		<xsl:value-of select="substring-before($input, $substr)"/>
		<xsl:if test="contains($temp, $substr)">
				<xsl:value-of select="$substr"/>
				<xsl:call-template name="substring-before-last">
						<xsl:with-param name="input" select="$temp"/>
						<xsl:with-param name="substr" select="$substr"/>
				</xsl:call-template>
		</xsl:if>
	</xsl:if>
 </xsl:template>

<xsl:template name="paging">
	<!-- page variables and constants-->
	<xsl:variable name="r" select="//rows"/>
	<xsl:variable name="p" select="//page"/>
	<xsl:variable name="t" select="//result/@numFound"/>
	<xsl:variable name="tp" select="ceiling($t div $r)" />
	<!-- prev page  -->
	<xsl:if test="($p - 1) &gt; 0" >
		<xsl:element name="atom:link">
			<xsl:attribute name="rel">previous</xsl:attribute>
			<xsl:attribute name="href"><xsl:text>rss?</xsl:text><xsl:value-of select="//unparsedQuery"/>&amp;p=<xsl:value-of select="$p - 1" /></xsl:attribute>
		</xsl:element>
	</xsl:if>
<!-- next page  -->
	<xsl:if test="($p) &lt; $tp" >
		<xsl:element name="atom:link">
			<xsl:attribute name="rel">next</xsl:attribute>
			<xsl:attribute name="href"><xsl:text>rss?</xsl:text><xsl:value-of select="//unparsedQuery"/>&amp;p=<xsl:value-of select="$p + 1" /></xsl:attribute>
		</xsl:element>
	</xsl:if>
</xsl:template>

</xsl:stylesheet>
