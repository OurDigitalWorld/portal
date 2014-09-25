<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    
    <xsl:output method="text" omit-xml-declaration="yes" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <xsl:value-of select="//document/response/result/@numFound"/>
    </xsl:template>
</xsl:stylesheet>
