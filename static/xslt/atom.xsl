<?xml version="1.0" ?>
<xsl:stylesheet 
	version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:georss="http://www.georss.org/georss" 
	xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
	xmlns:java="http://xml.apache.org/xslt/java"
	exclude-result-prefixes="java">

 <xsl:output encoding="UTF-8" indent="no" method="xml" omit-xml-declaration="yes"/>

 <!--Main Template-->
 <xsl:template match="/">
	<feed xmlns="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
		<title>OurOntario search</title>
		<subtitle>Welcome to the OurOntario Discovery Portal, a service of Knowledge Ontario.</subtitle>
		<xsl:element name="link">
			<xsl:attribute name="rel">self</xsl:attribute>
			<xsl:attribute name="type">application/atom+xml</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:text>http://search.ourontario.ca/atom?</xsl:text><xsl:value-of select="//unparsedQuery"/>
			</xsl:attribute>
			<xsl:text>&#160;</xsl:text>
		</xsl:element>
		
		<id>http://search.ourontario.ca/atom</id>
		<category term="Regional / North America / Canada / Ontario / Society and Culture" >&#160;</category>
		<!--<xsl:call-template name="currentTime"/>-->
		<author>
			<name>Knowledge Ontario</name>
		</author>
		<logo>http://search.ourontario.ca/atomtile_50x50.gif</logo>
		
		<xsl:variable name="r" select="//str[@name='rows']"/>
		<xsl:variable name="p" select="//page"/>
		<xsl:variable name="t" select="//result/@numFound"/>
		<xsl:variable name="tp" select="ceiling($t div $r)" />

		<opensearch:totalResults><xsl:value-of select="$t"/></opensearch:totalResults>
		<opensearch:startIndex><xsl:value-of select="//str[@name='start']"/></opensearch:startIndex>
		<opensearch:itemsPerPage><xsl:value-of select="$r"/></opensearch:itemsPerPage>
		<!-- may need to supply alternate values here -->
		<xsl:element name="opensearch:Query">
			<xsl:attribute name="role">request</xsl:attribute>
			<xsl:attribute name="searchTerms"><xsl:value-of select="//str[@name='q']"/></xsl:attribute>
			<xsl:text>&#160;</xsl:text>
		</xsl:element>
		
		<xsl:element name="link">
			<xsl:attribute name="rel">alternate</xsl:attribute>
			<xsl:attribute name="type">text/html</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:text>http://search.ourontario.ca/results?</xsl:text><xsl:value-of select="//unparsedQuery"/>
			</xsl:attribute>
			<xsl:text>&#160;</xsl:text>
		</xsl:element>
		<xsl:element name="link">
			<xsl:attribute name="rel">first</xsl:attribute>
			<xsl:attribute name="type">application/atom+xml</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:text>atom?</xsl:text><xsl:value-of select="//unparsedQuery"/><xsl:text>&amp;p=1</xsl:text>
			</xsl:attribute>
			<xsl:text>&#160;</xsl:text>
		</xsl:element>
		<xsl:if test="($p - 1) &gt; 0" >
			<xsl:element name="link">
				<xsl:attribute name="rel">previous</xsl:attribute>
				<xsl:attribute name="type">application/atom+xml</xsl:attribute>
				<xsl:attribute name="href">
					<xsl:text>atom?</xsl:text><xsl:value-of select="//unparsedQuery"/><xsl:text>&amp;p=</xsl:text><xsl:value-of select="$p - 1" />
				</xsl:attribute>
				&#160;
			</xsl:element>
		</xsl:if>
		<xsl:if test="($p) &lt; $tp" >
			<xsl:element name="link">
				<xsl:attribute name="rel">next</xsl:attribute>
				<xsl:attribute name="type">application/atom+xml</xsl:attribute>
				<xsl:attribute name="href">
					<xsl:text>atom?</xsl:text><xsl:value-of select="//unparsedQuery"/><xsl:text>&amp;p=</xsl:text><xsl:value-of select="$p + 1" />
				</xsl:attribute>
				<xsl:text>&#160;</xsl:text>
			</xsl:element>
		</xsl:if>
		<xsl:element name="link">
			<xsl:attribute name="rel">last</xsl:attribute>
			<xsl:attribute name="type">application/atom+xml</xsl:attribute>
			<xsl:attribute name="href">
				<xsl:text>atom?</xsl:text><xsl:value-of select="//unparsedQuery"/><xsl:text>&amp;p=</xsl:text><xsl:value-of select="$tp" />
			</xsl:attribute>
			<xsl:text>&#160;</xsl:text>
		</xsl:element>
		<link rel="search" type="application/opensearchdescription+xml" title="AlouetteCanada" href="opensearch" >&#160;</link>
		<xsl:for-each select="//response/result/doc">
			<xsl:call-template name="document"/>
		</xsl:for-each>
	</feed>
 </xsl:template>

 <!-- process each record -->
 <xsl:template name="document">
	<entry xmlns="http://www.w3.org/2005/Atom">
		<title>
			<xsl:value-of select="./arr[@name='title']"/>
		</title>
		<xsl:call-template name="summary"/>
		<xsl:element name="link">
			<xsl:attribute name="rel">alternate</xsl:attribute>
			<xsl:attribute name="href"><xsl:value-of select="str[@name='url']" /></xsl:attribute>
			&#160;
		</xsl:element>
		<xsl:element name="id"><xsl:value-of select="str[@name='url']" /></xsl:element>
		<xsl:for-each select="./arr[@name='creator']">
			<author><name><xsl:value-of select="." /></name></author>
		</xsl:for-each>
		<xsl:if test="string-length(float[@name='itemLatitude']) &gt; 0">
			<georss:point>
				<xsl:value-of select="float[@name='itemLatitude']" />
				<xsl:text> </xsl:text>
				<xsl:value-of select="float[@name='itemLongitude']" />
			</georss:point>
		</xsl:if>

		<updated>
			<xsl:choose>
				<xsl:when test="string-length(date[@name='madePublic']) &gt; 0">
					<xsl:value-of select="date[@name='madePublic']" />
				</xsl:when>
				<xsl:when test="string-length(date[@name='modified']) &gt; 0">
					<xsl:value-of select="date[@name='modified']" />
				</xsl:when>
				<xsl:when test="string-length(date[@name='created']) &gt; 0">
					<xsl:value-of select="date[@name='created']" />
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>2008-08-08T23:21:00Z</xsl:text>
				</xsl:otherwise>
			</xsl:choose>
		</updated>
	</entry>
 </xsl:template>

 <xsl:template name="summary">
	<summary type="html" xmlns="http://www.w3.org/2005/Atom">
	<xsl:text disable-output-escaping="yes">&amp;lt;img src=&quot;</xsl:text>
	<xsl:value-of select="str[@name='thumbnail']" />
	<xsl:text disable-output-escaping="yes">&quot; alt=&quot;</xsl:text>
	<xsl:value-of select="./arr[@name='title']"/>
	<xsl:text disable-output-escaping="yes">&quot; /&amp;gt;</xsl:text>
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
	<xsl:value-of select="$mydescription"/>
	</summary>
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

<!--<xsl:template name="replace-string">
	<xsl:param name="text"/>
	<xsl:param name="from"/>
	<xsl:param name="to"/>
	<xsl:choose>
		<xsl:when test="contains($text, $from)">
			<xsl:variable name="before" select="substring-before($text, $from)"/>
			<xsl:variable name="after" select="substring-after($text, $from)"/>
			<xsl:variable name="prefix" select="concat($before, $to)"/>
			<xsl:value-of select="$before"/>
			<xsl:value-of select="$to"/>
			<xsl:value-of select="$after"/>
		</xsl:when> 
		<xsl:otherwise>
			<xsl:value-of select="$text"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>-->

<xsl:template name="replaceCharsInString">
  <xsl:param name="stringIn"/>
  <xsl:param name="charsIn"/>
  <xsl:param name="charsOut"/>
  <xsl:choose>
    <xsl:when test="contains($stringIn,$charsIn)">
      <xsl:value-of select="concat(substring-before($stringIn,$charsIn),$charsOut)"/>
      <xsl:call-template name="replaceCharsInString">
        <xsl:with-param name="stringIn" select="substring-after($stringIn,$charsIn)"/>
        <xsl:with-param name="charsIn" select="$charsIn"/>
        <xsl:with-param name="charsOut" select="$charsOut"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$stringIn"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!--<xsl:template name="currentTime" 
              xmlns:date="java:java.util.Date">
  <xsl:value-of select="date:new()"/>
   2008-08-08T23:21:00Z
</xsl:template>
-->
<xsl:template name="currentTime">
	<xsl:variable name="javaformat">
		<xsl:text>EEE MMM dd HH:mm:ss zzz yyyy</xsl:text>
	</xsl:variable>
	<xsl:variable name="theDate">
		<xsl:value-of select="java:java.util.Date.new()"/>
		<!--Mon Sep 29 11:02:50 EDT 2008-->
	</xsl:variable>
	<xsl:variable name="atomformat">
		<xsl:text>yyyy-MM-dd'T'HH:mm:ss'Z'</xsl:text>
	</xsl:variable>

	<updated xmlns="http://www.w3.org/2005/Atom">
		<xsl:value-of select="java:dateUtil.reFormat($javaformat, $atomformat, $theDate)" /> 
	</updated>
</xsl:template>

</xsl:stylesheet>
