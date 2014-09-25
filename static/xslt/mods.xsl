<?xml version="1.0" ?>
<xsl:stylesheet 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:georss="http://www.georss.org/georss">

 <xsl:output encoding="UTF-8" indent="no"/>

 <!--Main Template-->
 <xsl:template match="/">
	 <modsCollection>
	<xsl:for-each select="//response/result/doc">
		<xsl:call-template name="mods"/>
	</xsl:for-each>
	</modsCollection>
 </xsl:template>

 <xsl:template name="mods">
	<mods > 
		<location>
			<url><xsl:value-of select="str[@name='url']" /></url>
		</location>
		<titleInfo>
			<title><xsl:value-of select="./arr[@name='title']/str"/></title>
		</titleInfo>
		<xsl:if test="string-length(arr[@name='creator']) &gt; 0 or string-length(arr[@name='contributor']) &gt; 0">
			<name>
				<xsl:if test="string-length(arr[@name='creator']) &gt; 0">
					<namePart><xsl:value-of select="./arr[@name='creator']/str"/></namePart>
				</xsl:if>
				<xsl:if test="string-length(arr[@name='contributor']) &gt; 0">
					<xsl:for-each select="arr[@name='contributor']/str">
						<namePart><xsl:value-of select="./arr[@name='contributor']/str"/></namePart>
					</xsl:for-each>
				</xsl:if>
			</name>
		</xsl:if>

		<xsl:if test="string-length(arr[@name='source']) &gt; 0">
			<relatedItem type="original"> 
				<xsl:value-of select="./arr[@name='source']/str"/>
			</relatedItem>
		</xsl:if>

		<xsl:if test="string-length(arr[@name='publisher']) &gt; 0 or string-length(date[@name='madePublic']) &gt; 0 or string-length(arr[@name='temporal']) &gt; 0">
			<originInfo>
				<xsl:if test="string-length(arr[@name='publisher']) &gt; 0">
					<publisher><xsl:value-of select="./arr[@name='publisher']/str"/></publisher>
				</xsl:if>
				<xsl:if test="string-length(arr[@name='temporal']) &gt; 0">
					<dateCreated><xsl:value-of select="./arr[@name='temporal']/str"/></dateCreated>
				</xsl:if>
				<xsl:if test="string-length(date[@name='madePublic']) &gt; 0">
					<dateIssued><xsl:value-of select="date[@name='madePublic']" /> </dateIssued>
				</xsl:if>
			</originInfo>
		</xsl:if>

		<abstract>
			<xsl:value-of select="./arr[@name='description']"/><xsl:text> </xsl:text>
		</abstract>

		<xsl:if test="string-length(arr[@name='subject']) &gt; 0 or string-length(arr[@name='spatial']) &gt; 0">
			<xsl:for-each select="arr[@name='subject']/str">
				<subject><topic><xsl:value-of select="."/></topic></subject>
			</xsl:for-each>
			<xsl:if test="string-length(arr[@name='spatial']) &gt; 0">
				<subject><geographic><xsl:value-of select="./arr[@name='spatial']"/></geographic></subject>
			</xsl:if>
		</xsl:if>
		<typeOfResource>
			<xsl:choose>
				<xsl:when test="arr[@name='type'] = 'image'">still image</xsl:when>
				<xsl:when test="arr[@name='type'] = 'video'">moving image</xsl:when>
				<xsl:when test="arr[@name='type'] = 'audio'">sound recording</xsl:when>
				<xsl:otherwise><xsl:value-of select="arr[@name='type']" /></xsl:otherwise>
			</xsl:choose>
		</typeOfResource>
		<recordInfo>
			<xsl:for-each select="./arr[@name='site']/str">
				<recordContentSource><xsl:value-of select="."/></recordContentSource>
			</xsl:for-each>
		</recordInfo>
		<xsl:if test="string-length(arr[@name='language']) &gt; 0">
			<language>
				<languageTerm><xsl:value-of select="./arr[@name='language']"/></languageTerm>
			</language>
		</xsl:if>
	</mods>
</xsl:template>
</xsl:stylesheet>