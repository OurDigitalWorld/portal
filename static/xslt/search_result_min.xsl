<?xml version="1.0" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:georss="http://www.georss.org/georss"
	version="1.0">
	<xsl:output method="html"/>
	<xsl:variable name="resultCount">
		<xsl:value-of select="//result/@numFound"/>
	</xsl:variable>
	<xsl:variable name="geoCount">
		<xsl:value-of select="//geoCount//result/@numFound"/>
	</xsl:variable>
	<xsl:variable name="start">
		<xsl:value-of select="/response//result/@start"/>
	</xsl:variable>
	<xsl:variable name="rows">
		<xsl:value-of select="//str[@name='rows']"/>
	</xsl:variable>
	<xsl:param name="unparsedQuery" />
	<xsl:param name="page"/>


	<xsl:variable name="icon_audio">icon_audio.jpg</xsl:variable>
	<xsl:variable name="icon_collection">icon_collection.jpg</xsl:variable>
	<xsl:variable name="icon_image">icon_image.jpg</xsl:variable>
	<xsl:variable name="icon_object">icon_object.jpg</xsl:variable>
	<xsl:variable name="icon_text">icon_text.jpg</xsl:variable>
	<xsl:variable name="icon_video">icon_video.jpg</xsl:variable>
	<xsl:variable name="icon_comment">icon_comment.gif</xsl:variable>
	<xsl:variable name="icon_mystery">icon_mystery.gif</xsl:variable>
	<xsl:variable name="sort_hits">sort_hits.gif</xsl:variable>
	<xsl:variable name="sort_year">sort_year.gif</xsl:variable>
	<xsl:variable name="sort_AZ">sort_AZ.gif</xsl:variable>
	<xsl:variable name="HS_hide">HS_hide.gif</xsl:variable>
	<xsl:variable name="HS_see">HS_see.gif</xsl:variable>

	<xsl:variable name="styleConstant">84</xsl:variable>
	<xsl:variable name="tag1">85</xsl:variable>
	<xsl:variable name="tag2">100</xsl:variable>
	<xsl:variable name="tag3">115</xsl:variable>
	<xsl:variable name="tag4">135</xsl:variable>
	<xsl:variable name="tag5">155</xsl:variable>
	<xsl:variable name="tag6">165</xsl:variable>
	<xsl:variable name="tag7">180</xsl:variable>

	<!--Main Template-->
	<xsl:template match="/">
		<xsl:call-template name="searchLogic" />

		<xsl:choose>
			<xsl:when test="$resultCount &gt; 0">
				<div class="right">
					<div class="pagination"><xsl:call-template name="paging"/></div><!---->

					<xsl:for-each select="//response/result/doc">
						<xsl:call-template name="document"/>
					</xsl:for-each>
					<div class="pagination"><xsl:call-template name="paging"/></div>
				</div>
				<div class="left">
					<form class="easyform" name="Search" action="results" method="get">
						<fieldset class="externalResults"> </fieldset>
						<fieldset>
							<legend>Search within these results</legend>
							<input type="text" class="q" name="q" size="20"/>
							<input type="submit" name="submit" value="Go"/>
						</fieldset>
						<fieldset>
							<legend>Media Types</legend>
							<ul class="options">
								<li class="option-type-audio">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">audio</xsl:with-param>
										<xsl:with-param name="mtLabel">Audio</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-collection">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">collection</xsl:with-param>
										<xsl:with-param name="mtLabel">Collection</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-genealogy">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">genealogical
											resource</xsl:with-param>
										<xsl:with-param name="mtLabel">Genealogical
											Resource</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-images">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">image</xsl:with-param>
										<xsl:with-param name="mtLabel">Image</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-newspaper">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">newspaper</xsl:with-param>
										<xsl:with-param name="mtLabel">Newspaper</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-object">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">object</xsl:with-param>
										<xsl:with-param name="mtLabel">Object</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-text">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">text</xsl:with-param>
										<xsl:with-param name="mtLabel">Text</xsl:with-param>
									</xsl:call-template>
								</li>
								<li class="option-type-video">
									<xsl:call-template name="mediaType">
										<xsl:with-param name="mt">video</xsl:with-param>
										<xsl:with-param name="mtLabel">Video</xsl:with-param>
									</xsl:call-template>
								</li>
							</ul>
						</fieldset>

						<fieldset>
							<xsl:call-template name="Contributors"/>
						</fieldset>
						<xsl:if
							test="(string-length(//lst[@name='fSpatial']) &gt; 0) and (//lst[@name='fSpatial'] != 'null')">
							<fieldset>
								<xsl:call-template name="Location"/>
							</fieldset>
						</xsl:if>
						<xsl:if
							test="(string-length(//lst[@name='fGroupName']) &gt; 0) and (//lst[@name='fGroupName'] != 'null')">
							<fieldset>
								<xsl:call-template name="GroupName"/>
							</fieldset>
						</xsl:if>
						<xsl:if
							test="(string-length(//lst[@name='itemType']) &gt; 0) and (//lst[@name='itemType'] != 'null')">
							<fieldset>
								<xsl:call-template name="ItemType"/>
							</fieldset>
						</xsl:if>
						<xsl:if
							test="((//lst[@name='featureComment']/int[@name='true'] &gt; 0) or (//lst[@name='featureMystery']/int[@name='true'] &gt; 0))">
							<fieldset>
								<xsl:call-template name="Feature"/>
							</fieldset>
						</xsl:if>
						<fieldset>
							<xsl:call-template name="translate"/>
						</fieldset>
					</form>
				</div>
			</xsl:when>
			<xsl:otherwise>
				<div class="noResults">No Results were found.<br/>
					<!-- try to relax the constraints (OR) -->
					<xsl:element name="a">
						<xsl:attribute name="href">
							<!--xsl:text>results?</xsl:text><xsl:value-of select="$unparsedQuery"/>&amp;bl=or-->
							<xsl:text>results?</xsl:text>
						</xsl:attribute> Try this search again with relaxed constraints! (<a
							href="help#relax">What is this?</a>) </xsl:element>
					<br/>
					<!-- try a fuzzier query -->
					<xsl:element name="a">
						<xsl:attribute name="href">
							<!--xsl:text>results?</xsl:text><xsl:value-of select="$unparsedQuery"/><xsl:text>&amp;fz=1</xsl:text-->
							<xsl:text>results?</xsl:text>
						</xsl:attribute> Try this search again but fuzzier! (<a href="help#fuzzy"
							>What is this?</a>) </xsl:element>
					<br/>
					<form action="results" method="get" class="SearchForm" name="Search"> New
						Search: <input type="text" name="q" size="50"/>
						<input type="submit" value="Go" class="SearchGo"/>
					</form>
				</div>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>

	<!-- Start of supporting templates and variable calculations-->
	<xsl:template name="searchLogic">
	<div class="searchLogic">
		<xsl:if test="//altTermFromCollation">
			<div class="alert">
				Your search for <b><xsl:value-of select="//query" /></b> returned no results. We substituted <b><xsl:value-of select="//altTermFromCollation" /></b>.<br/>
			</div>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="$resultCount = 1">
				We found <b class="count">1</b> matching item.<br />
			</xsl:when>
			<xsl:otherwise>
				We found <b class="count"> <xsl:value-of select="//result/@numFound"/></b>  matching items.<br />
			</xsl:otherwise>
		</xsl:choose>
	</div>
	</xsl:template>
	<!-- Results set templates  for each returned document -->
	<xsl:template name="document">
		<xsl:element name="div">
			<xsl:attribute name="class">result clearfix</xsl:attribute>
			<xsl:attribute name="about">
				<xsl:value-of select="./str[@name='url']"/>
			</xsl:attribute>
			<xsl:call-template name="url"/>
			<h4>
				<xsl:call-template name="Title"/>
			</h4>
			<p>
				<xsl:call-template name="Description"/>
			</p>
			<p>
				<xsl:call-template name="docParts"/>
			</p>
			<p>
				<b>
					<xsl:call-template name="Site"/>
				</b>
			</p>
		</xsl:element>
	</xsl:template>
	<xsl:template name="url">
		<xsl:element name="a">
			<xsl:attribute name="href">
				<xsl:value-of select="./str[@name='url']"/>
			</xsl:attribute>
			<xsl:element name="img">
				<xsl:attribute name="src">
					<xsl:value-of select="./str[@name='thumbnail']"/>
				</xsl:attribute>
				<xsl:attribute name="class">result</xsl:attribute>
				<xsl:attribute name="alt"><xsl:value-of select="./arr[@name='title']"
						/>&#160;<xsl:value-of select="./str[@name='description']"/></xsl:attribute>

			</xsl:element>
		</xsl:element>
	</xsl:template>
	<xsl:template name="Title">
		<xsl:element name="abbr">
			<xsl:attribute name="class">unapi-id</xsl:attribute>
			<xsl:attribute name="title">
				<xsl:value-of select="./str[@name='id']"/>
			</xsl:attribute>
		</xsl:element>

		<xsl:element name="a">
			<xsl:attribute name="href">
				<xsl:value-of select="./str[@name='url']"/>
			</xsl:attribute>
			<div property="dc:title">
				<xsl:value-of select="./arr[@name='title']"/>
			</div>
		</xsl:element>

		<!--div class="filesize"> - <xsl:value-of select="format-number(./str[@name='fileSize'] div 1024, '#.0')"/> K</div-->
	</xsl:template>

	<xsl:template name="Site">
		<xsl:for-each select="./arr[@name='site']/str">
			<xsl:value-of select="."/>
			<br/>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="Description">
		<div property="dc:description">
			<xsl:value-of select="./arr[@name='bibliographicCitation']"
				disable-output-escaping="yes"/>
			<xsl:text>&#160;&#160;</xsl:text>
			<xsl:variable name="mydescription">
				<xsl:variable name="maxlen">300</xsl:variable>
				<xsl:choose>
					<xsl:when test="string-length(./arr[@name='description']) &lt;= $maxlen">
						<xsl:value-of select="./arr[@name='description']"
							disable-output-escaping="yes"/>
					</xsl:when>
					<xsl:when test="not(contains(./arr[@name='description'],' '))">
						<xsl:value-of select="substring(./arr[@name='description'],0,$maxlen)"
							disable-output-escaping="yes"/>
						<xsl:text>...</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="substring-before-last">
							<xsl:with-param name="input"
								select="substring(
				./arr[@name='description'],0,$maxlen)"/>
							<xsl:with-param name="substr" select="' '"/>
						</xsl:call-template>
						<xsl:text>...</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>
			<xsl:value-of select="$mydescription"/>
		</div>
		<!--div class="snippet">
		<xsl:variable name="id" select="./str[@name='id']"/>
		<xsl:if test="string-length(//lst[@name=$id]/arr[@name='title']/str)  &lt; 1 and string-length(//lst[@name=$id]/arr[@name='linktext']/str) &gt; 0">
			..<xsl:value-of select="//lst[@name=$id]/arr[@name='linktext']/str" disable-output-escaping="yes"/>...
		</xsl:if>
	</div-->
		<xsl:if test="string-length(./float[@name='itemLatitude']) &gt; 0">
			<div class="geo">
				<span class="latitude"><xsl:value-of select="float[@name='itemLatitude']"/></span>,
					<span class="longitude"><xsl:value-of select="float[@name='itemLongitude']"
					/></span>
				<!--<geo:Point>-->
				<geo:lat><xsl:value-of select="float[@name='itemLatitude']"/></geo:lat>
				<geo:long><xsl:value-of select="float[@name='itemLongitude']"/></geo:long>
				<!--</geo:Point>-->
			</div>
			<div class="hidden"> </div>
		</xsl:if>
	</xsl:template>

	<xsl:template name="docParts">
		<xsl:if test="./parts/response/result/@numFound &gt; 0">
			<xsl:variable name="baseURL">
				<xsl:value-of select="./str[@name='url']"/>
			</xsl:variable>
			<div class="docParts">
				<div class="docPartsLabel">Pages/Parts:</div>
				<xsl:for-each select="./parts/response/result/doc">
					<xsl:variable name="localPartID">
						<xsl:value-of select="./str[@name='id']"/>
					</xsl:variable>
					<xsl:variable name="localHighlight">
						<xsl:value-of
							select="concat(substring-before(//parts/response/lst[@name='highlighting']/lst[@name=$localPartID]/arr/str,'&lt;em&gt;'),substring-after(//parts/response/lst[@name='highlighting']/lst[@name=$localPartID]/arr/str,'&lt;em&gt;'))"
						/>
					</xsl:variable>
					<div class="docPart">
						<xsl:element name="a">
							<xsl:attribute name="href">
								<xsl:choose>
									<xsl:when test="contains(./str[@name='partURL'], 'http')">
										<xsl:value-of select="./str[@name='partURL']"/>
									</xsl:when>
									<xsl:otherwise>
										<xsl:value-of select="substring-before($baseURL, 'data')"
											/>page/<xsl:value-of select="./int[@name='partSort']"/>
									</xsl:otherwise>
								</xsl:choose>
							</xsl:attribute>
							<xsl:attribute name="title"> ... <xsl:value-of
									select="concat(substring-before($localHighlight,'&lt;/em&gt;'),substring-after($localHighlight,'&lt;/em&gt;'))"
								/> ... </xsl:attribute>
							<xsl:value-of select="./str[@name='label']"/>
						</xsl:element>
					</div>
				</xsl:for-each>
			</div>
		</xsl:if>
		<xsl:if test="./parts/response/result/@numFound &gt; 10">
			<div class="docPartAll">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:value-of
							select="./parts/response/result/doc//str[@name='docid']"
							/>/toc?q=<xsl:value-of select="//partsQ"/>
					</xsl:attribute>
					<xsl:attribute name="title"> More pages/parts </xsl:attribute> [See the entire
						<xsl:value-of select="./parts/response/result/@numFound"/> pages/parts]
				</xsl:element>
			</div>
		</xsl:if>
	</xsl:template>


	<xsl:template name="paging">
		<!-- page variables and constants-->
		<xsl:variable name="r" select="$rows"/>
		<xsl:variable name="p" select="$page"/>
		<xsl:variable name="t" select="$resultCount"/>
		<xsl:variable name="tp" select="ceiling($t div $r)"/>

		<!-- current page -->

		<span>Page <xsl:value-of select="$p"/> of <xsl:value-of select="$tp"/>
		</span>

		<!-- prev page  -->
		<xsl:choose>
			<xsl:when test="($p - 1) &gt; 0">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p - 1"/>
					</xsl:attribute> &#x2190; Prev </xsl:element>
			</xsl:when>
		</xsl:choose>

		<!-- page 1 if not in current display -->
		<xsl:choose>
			<xsl:when test="($p - 3) &gt; 0">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="1"/>
					</xsl:attribute>
					<xsl:value-of select="1"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>

		<!-- page 2 if not in current display -->
		<xsl:choose>
			<xsl:when test="($p - 3) &gt; 1">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="2"/>
					</xsl:attribute>
					<xsl:value-of select="2"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>

		<!-- skip a few if page 3 not in current display -->
		<xsl:choose>
			<xsl:when test="($p - 3) &gt; 2"> ... </xsl:when>
		</xsl:choose>

		<xsl:choose>
			<xsl:when test="($p - 2) &gt; 0">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p - 2"/>
					</xsl:attribute>
					<xsl:value-of select="$p - 2"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>
		<xsl:choose>
			<xsl:when test="($p - 1) &gt; 0">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p - 1"/>
					</xsl:attribute>
					<xsl:value-of select="$p - 1"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>
		<!-- current page 
			suppress when only one-->

		<xsl:choose>
			<xsl:when test="$tp != 1"> &#160;<big><xsl:value-of select="$p"/></big>&#160;
			</xsl:when>
		</xsl:choose>

		<!-- next page  -->
		<xsl:choose>
			<xsl:when test="($p) &lt; $tp">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p + 1"/>
					</xsl:attribute>
					<xsl:value-of select="$p + 1"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>
		<!-- page after next  -->
		<xsl:choose>
			<xsl:when test="($p + 1) &lt; $tp">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p + 2"/>
					</xsl:attribute>
					<xsl:value-of select="$p + 2"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>

		<!-- skip a few if not two pages or less from the end  -->
		<xsl:choose>
			<xsl:when test="($p + 2) &lt; ($tp - 2)"> ... </xsl:when>
		</xsl:choose>

		<!-- penultimate page if more than 2 from the end-->
		<xsl:choose>
			<xsl:when test="($p + 2) &lt; ($tp - 1)">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$tp - 1"/>
					</xsl:attribute>
					<xsl:value-of select="$tp - 1"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>
		<!-- last page if more than 3 from the end-->
		<xsl:choose>
			<xsl:when test="($p + 3) &lt; ($tp + 1)">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$tp"/>
					</xsl:attribute>
					<xsl:value-of select="$tp"/>
				</xsl:element>
			</xsl:when>
		</xsl:choose>

		<!-- next page-->
		<xsl:choose>
			<xsl:when test="($p + 1) &lt; $tp + 1">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?</xsl:text><xsl:value-of
							select="$unparsedQuery"/>&amp;p=<xsl:value-of select="$p + 1"/>
					</xsl:attribute> Next &#x2192;</xsl:element>
			</xsl:when>
		</xsl:choose>
	</xsl:template>


	<xsl:template name="mediaType">
		<xsl:param name="mt"/>
		<xsl:param name="mtLabel"/>
		<xsl:choose>
			<xsl:when test="//lst[@name='type']/int[@name=$mt]">
				<xsl:element name="a">
					<xsl:attribute name="href"><xsl:text>results?mt=</xsl:text><xsl:value-of
							select="$mt"/><xsl:text>&amp;</xsl:text><xsl:value-of
							select="$unparsedQuery"/>
					</xsl:attribute><xsl:value-of select="$mtLabel"/> (<xsl:value-of
						select="//lst[@name='type']/int[@name=$mt]"/>) </xsl:element>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$mtLabel"/> (0) </xsl:otherwise>
		</xsl:choose>
	</xsl:template>


	<xsl:template name="Contributors">
		<xsl:for-each
			select="//response/lst[@name='facet_counts']/lst[@name='facet_fields']/lst[@name='site']">
			<legend>Contributors</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 6 and //siteMore != 1">
					<xsl:call-template name="ListBrief">
						<xsl:with-param name="listName">site</xsl:with-param>
						<xsl:with-param name="listSolr">site</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="count(descendant::*) &lt; 7">
					<xsl:call-template name="ListShort">
						<xsl:with-param name="listName">site</xsl:with-param>
						<xsl:with-param name="listSolr">site</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="ListFull">
						<xsl:with-param name="listName">site</xsl:with-param>
						<xsl:with-param name="listSort" select="//siteSort"/>
						<xsl:with-param name="listSolr">site</xsl:with-param>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<!--  Block of Location/Spatial templates -->
	<xsl:template name="Location">
		<xsl:for-each select="//lst[@name='fSpatial']">
			<legend>Locations</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 10 and //lcmore != 1">
					<ul class="options">
						<xsl:call-template name="LocationBrief"/>
					</ul>
				</xsl:when>
				<xsl:when test="count(descendant::*) &gt; 10">
					<xsl:call-template name="LocationComplex"/>
				</xsl:when>
				<xsl:otherwise>
					<ul class="options">
						<xsl:call-template name="LocationSimple"/>
					</ul>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="LocationSimple">
		<xsl:for-each select="./int">
			<xsl:if test="normalize-space(./@name)">
				<xsl:element name="li">
					<xsl:element name="a">
						<xsl:attribute name="href"><xsl:text>results?lc=</xsl:text><xsl:value-of
								select="./@name"/>&amp;<xsl:value-of select="$unparsedQuery"/>
						</xsl:attribute>
						<xsl:value-of select="./@name"/>&#160;(<xsl:value-of select="."/>)
					</xsl:element>
				</xsl:element>
			</xsl:if>
		</xsl:for-each>

		<xsl:call-template name="UnidentifiedLocationCount"/>
	</xsl:template>

	<xsl:template name="LocationBrief">
		<xsl:for-each select="./int">
			<xsl:if test="normalize-space(./@name)">
				<xsl:if test="position() &lt; 7">
					<xsl:element name="li">
						<xsl:element name="a">
							<xsl:attribute name="href"><xsl:text>results?lc=</xsl:text><xsl:value-of
									select="./@name"/>&amp;<xsl:value-of select="$unparsedQuery"/>
							</xsl:attribute>
							<xsl:value-of select="./@name"/>&#160;(<xsl:value-of select="."/>)
						</xsl:element>
					</xsl:element>
				</xsl:if>
			</xsl:if>
		</xsl:for-each>
		<xsl:element name="li">
			<xsl:element name="a">
				<xsl:attribute name="href">
					<xsl:text>results?lcmore=1&amp;</xsl:text>
					<xsl:call-template name="replace-string">
						<xsl:with-param name="text" select="$unparsedQuery"/>
						<xsl:with-param name="from">lcmore=0</xsl:with-param>
						<xsl:with-param name="to"/>
					</xsl:call-template>
				</xsl:attribute>
				<xsl:element name="img">
					<xsl:attribute name="src">
						<xsl:value-of select="$HS_see"/>
					</xsl:attribute>
					<xsl:attribute name="alt">See the rest</xsl:attribute>
				</xsl:element>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template name="LocationComplex">
		<xsl:element name="a">
			<xsl:attribute name="href">
				<xsl:text>results?lcmore=0&amp;</xsl:text>
				<xsl:call-template name="replace-string">
					<xsl:with-param name="text" select="$unparsedQuery"/>
					<xsl:with-param name="from">lcmore=1</xsl:with-param>
					<xsl:with-param name="to"/>
				</xsl:call-template>
			</xsl:attribute>
			<xsl:element name="img">
				<xsl:attribute name="src">
					<xsl:value-of select="$HS_hide"/>
				</xsl:attribute>
				<xsl:attribute name="alt">Hide</xsl:attribute>
			</xsl:element>
		</xsl:element>
		<div class="tagcloud rightBox" id="subjects">
			<!-- start at first of branch -->
			<xsl:for-each select="./int">
				<xsl:sort select="@name"/>
				<xsl:if test="normalize-space(./@name)">
					<xsl:element name="a">
						<xsl:attribute name="href"><xsl:text>results?lc=</xsl:text><xsl:value-of
								select="./@name"/>&amp;<xsl:value-of select="$unparsedQuery"/>
						</xsl:attribute>
						<xsl:attribute name="style"><xsl:text>font-size:</xsl:text>
							<xsl:choose>
								<xsl:when test=". &lt; 5">
									<xsl:value-of select="$tag1"/>
								</xsl:when>
								<xsl:when test=". &gt; 4 and . &lt; 10">
									<xsl:value-of select="$tag2"/>
								</xsl:when>
								<xsl:when test=". &gt; 9 and . &lt; 20">
									<xsl:value-of select="$tag3"/>
								</xsl:when>
								<xsl:when test=". &gt; 19 and . &lt; 40">
									<xsl:value-of select="$tag4"/>
								</xsl:when>
								<xsl:when test=". &gt; 39 and . &lt; 100">
									<xsl:value-of select="$tag5"/>
								</xsl:when>
								<xsl:when test=". &gt; 99 and . &lt; 500">
									<xsl:value-of select="$tag5"/>
								</xsl:when>
								<xsl:when test=". &gt; 499">
									<xsl:value-of select="$tag6"/>
								</xsl:when>
							</xsl:choose><xsl:text>%</xsl:text>
						</xsl:attribute>
						<xsl:if test=". &lt; 8">
							<xsl:attribute name="class">subthreshold</xsl:attribute>
						</xsl:if>
						<xsl:value-of select="./@name"/>&#160;(<xsl:value-of select="."/>)
					</xsl:element>
				</xsl:if>
			</xsl:for-each>
		</div>
		<xsl:call-template name="UnidentifiedLocationCount"/>
		<xsl:element name="a">
			<xsl:attribute name="href">
				<xsl:text>results?lcmore=0&amp;</xsl:text>
				<xsl:call-template name="replace-string">
					<xsl:with-param name="text" select="$unparsedQuery"/>
					<xsl:with-param name="from">lcmore=1</xsl:with-param>
					<xsl:with-param name="to"/>
				</xsl:call-template>
			</xsl:attribute>
			<xsl:element name="img">
				<xsl:attribute name="src">
					<xsl:value-of select="$HS_hide"/>
				</xsl:attribute>
				<xsl:attribute name="alt">Hide</xsl:attribute>
			</xsl:element>
		</xsl:element>
	</xsl:template>

	<xsl:template name="UnidentifiedLocationCount">
		<xsl:variable name="NullLocation1" select="./int[@name = '']"/>
		<xsl:variable name="result1">
			<xsl:choose>
				<xsl:when test="contains(number($NullLocation1),'NaN')">
					<xsl:text>0</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$NullLocation1"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="NullLocation2" select="./int[position() = last()]"/>
		<xsl:variable name="result2">
			<xsl:choose>
				<xsl:when test="contains(number($NullLocation2),'NaN')">
					<xsl:text>0</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$NullLocation2"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>

		<xsl:variable name="resultFinal" select="$result1 + $result2"/>
		<xsl:if test="$resultFinal &gt; 0">
			<div class="facetpanelcontentelement">Location unidentified: <xsl:value-of
					select="$resultFinal"/>
			</div>
		</xsl:if>
	</xsl:template>

	<!--  Item Types -->

	<xsl:template name="ItemType">
		<xsl:for-each
			select="//lst[@name='facet_counts']/lst[@name='facet_fields']/lst[@name='itemType']">
			<xsl:if test="node()">
				<legend>Item types</legend>
				<div class="tagcloud rightBox">
					<!-- start at first of branch -->
					<xsl:for-each select="./int">
						<xsl:sort select="@name"/>
						<xsl:if test="normalize-space(./@name)">
							<xsl:element name="a">
								<xsl:attribute name="href"
										><xsl:text>results?itype=</xsl:text><xsl:value-of
										select="./@name"/>&amp;<xsl:value-of
										select="$unparsedQuery"/>
								</xsl:attribute>
								<xsl:attribute name="style"><xsl:text>font-size:</xsl:text>
									<xsl:choose>
										<xsl:when test=". &lt; 5">
											<xsl:value-of select="$tag1"/>
										</xsl:when>
										<xsl:when test=". &gt; 4 and . &lt; 10">
											<xsl:value-of select="$tag2"/>
										</xsl:when>
										<xsl:when test=". &gt; 9 and . &lt; 20">
											<xsl:value-of select="$tag3"/>
										</xsl:when>
										<xsl:when test=". &gt; 19 and . &lt; 40">
											<xsl:value-of select="$tag4"/>
										</xsl:when>
										<xsl:when test=". &gt; 39 and . &lt; 100">
											<xsl:value-of select="$tag5"/>
										</xsl:when>
										<xsl:when test=". &gt; 99 and . &lt; 500">
											<xsl:value-of select="$tag5"/>
										</xsl:when>
										<xsl:when test=". &gt; 499">
											<xsl:value-of select="$tag6"/>
										</xsl:when>
									</xsl:choose><xsl:text>%</xsl:text>
								</xsl:attribute>
								<xsl:value-of select="./@name"/>&#160;(<xsl:value-of select="."/>)
							</xsl:element>
						</xsl:if>
					</xsl:for-each>
				</div>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<!-- Facet Panel:  Features  -->
	<xsl:template name="Feature">
		<xsl:choose>
			<xsl:when test="(//lst[@name='featureComment']/int[@name='true'] &gt; 0)">
				<legend>Features</legend>
			</xsl:when>
			<xsl:when test="(//lst[@name='featureMystery']/int[@name='true'] &gt; 0)">
				<legend>Features</legend>
			</xsl:when>
		</xsl:choose>
		<ul class="options">
			<xsl:for-each select="//lst">
				<xsl:if test="count(self::node()[@name='featureComment']/*) &gt; 0">
					<xsl:for-each select="./int">
						<xsl:if test="./@name = 'true'">
							<xsl:element name="li">
								<xsl:element name="a">
									<xsl:attribute name="href"
											><xsl:text>results?fc=true</xsl:text>&amp;<xsl:value-of
											select="$unparsedQuery"/>
									</xsl:attribute>
									<xsl:element name="img"><xsl:attribute name="src"><xsl:value-of
												select="$icon_comment"
											/></xsl:attribute><xsl:attribute name="alt"
											><xsl:text>comment</xsl:text></xsl:attribute></xsl:element>&#160;<xsl:text>Comments</xsl:text>&#160;(<xsl:value-of
										select="."/>) </xsl:element>
							</xsl:element>
						</xsl:if>
					</xsl:for-each>
				</xsl:if>
				<xsl:if test="count(self::node()[@name='featureMystery']/*) &gt; 0">
					<xsl:for-each select="./int">
						<xsl:if test="./@name = 'true'">
							<xsl:element name="li">
								<xsl:element name="a">
									<xsl:attribute name="href"
											><xsl:text>results?fm=true</xsl:text>&amp;<xsl:value-of
											select="$unparsedQuery"/>
									</xsl:attribute><xsl:element name="img"><xsl:attribute
											name="src"><xsl:value-of select="$icon_mystery"
											/></xsl:attribute><xsl:attribute name="alt"
											><xsl:text>mystery</xsl:text></xsl:attribute></xsl:element>&#160;<xsl:text>Mysteries</xsl:text>&#160;(<xsl:value-of
										select="."/>) </xsl:element>
							</xsl:element>
						</xsl:if>
					</xsl:for-each>
				</xsl:if>
			</xsl:for-each>
		</ul>
	</xsl:template>
	<xsl:template name="Source">
		<xsl:for-each select="//lst[@name='fSource']">
			<legend>Ministry/Agency</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 6 and //sourceMore != 1">
					<xsl:call-template name="ListBrief">
						<xsl:with-param name="listName">source</xsl:with-param>
						<xsl:with-param name="listSolr">fSource</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="count(descendant::*) &lt; 7">
					<xsl:call-template name="ListShort">
						<xsl:with-param name="listName">source</xsl:with-param>
						<xsl:with-param name="listSolr">fSource</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="ListFull">
						<xsl:with-param name="listName">source</xsl:with-param>
						<xsl:with-param name="listSort" select="//sourceSort"/>
						<xsl:with-param name="listSolr">fSource</xsl:with-param>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="Creator">
		<xsl:for-each select="//lst[@name='fCreator']">
			<legend>Author</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 6 and //creatorMore != 1">
					<xsl:call-template name="ListBrief">
						<xsl:with-param name="listName">creator</xsl:with-param>
						<xsl:with-param name="listSolr">fCreator</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="count(descendant::*) &lt; 7">
					<xsl:call-template name="ListShort">
						<xsl:with-param name="listName">creator</xsl:with-param>
						<xsl:with-param name="listSolr">fCreator</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="ListFull">
						<xsl:with-param name="listName">creator</xsl:with-param>
						<xsl:with-param name="listSort" select="//creatorSort"/>
						<xsl:with-param name="listSolr">fCreator</xsl:with-param>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="Year">
		<xsl:for-each select="//lst[@name='dateNewest']">
			<legend>Years</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 6 and //yearMore != 1">
					<xsl:call-template name="ListBrief">
						<xsl:with-param name="listName">year</xsl:with-param>
						<xsl:with-param name="listSolr">dateNewest</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="count(descendant::*) &lt; 7">
					<xsl:call-template name="ListShort">
						<xsl:with-param name="listName">year</xsl:with-param>
						<xsl:with-param name="listSolr">dateNewest</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="ListFull">
						<xsl:with-param name="listName">year</xsl:with-param>
						<xsl:with-param name="listSort" select="//yearSort"/>
						<xsl:with-param name="listSolr">dateNewest</xsl:with-param>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="GroupName">
		<xsl:for-each select="//lst[@name='fGroupName']">
			<legend>Groups/Collections</legend>
			<xsl:choose>
				<xsl:when test="count(descendant::*) &gt; 6 and //grnMore != 1">
					<xsl:call-template name="ListBrief">
						<xsl:with-param name="listName">grn</xsl:with-param>
						<xsl:with-param name="listSolr">fGroupName</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="count(descendant::*) &lt; 7">
					<xsl:call-template name="ListShort">
						<xsl:with-param name="listName">grn</xsl:with-param>
						<xsl:with-param name="listSolr">fGroupName</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="ListFull">
						<xsl:with-param name="listName">grn</xsl:with-param>
						<xsl:with-param name="listSort" select="//grnSort"/>
						<xsl:with-param name="listSolr">fGroupName</xsl:with-param>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</xsl:template>


	<xsl:template name="translate">
		<center>
			<xsl:element name="script">
				<xsl:attribute name="src"
					>http://www.gmodules.com/ig/ifr?url=http://www.google.com/ig/modules/translatemypage.xml&amp;up_source_language=en&amp;w=160&amp;h=60&amp;title=&amp;border=&amp;output=js</xsl:attribute>
			</xsl:element>
		</center>
	</xsl:template>

	<xsl:template name="ListFull">
		<xsl:param name="listName"/>
		<xsl:param name="listSort"/>
		<xsl:param name="listSolr"/>
		<ul class="options">

			<xsl:for-each
				select="//response/lst[@name='facet_counts']/lst[@name='facet_fields']/lst[@name=$listSolr]">
				<div class="facetpanelcontentelement">
					<xsl:choose>
						<xsl:when test="$listSort = 'a'">
							<xsl:element name="li">
								<xsl:element name="a">
									<xsl:attribute name="href">
										<xsl:text>results?</xsl:text>
										<xsl:value-of select="$listName"/>
										<xsl:text>Sort=n&amp;</xsl:text>
										<xsl:call-template name="replace-string">
											<xsl:with-param name="text" select="$unparsedQuery"/>
											<xsl:with-param name="from"><xsl:value-of
												select="$listName"/>Sort=a</xsl:with-param>
											<xsl:with-param name="to"/>
										</xsl:call-template>
									</xsl:attribute>
									<xsl:element name="img">
										<xsl:attribute name="src">
											<xsl:value-of select="$sort_hits"/>
										</xsl:attribute>
										<xsl:attribute name="alt">Sort by Hit count</xsl:attribute>
									</xsl:element>
								</xsl:element>
							</xsl:element>
						</xsl:when>
						<xsl:otherwise>
							<xsl:element name="li">
								<xsl:element name="a">
									<xsl:attribute name="href">
										<xsl:text>results?</xsl:text>
										<xsl:value-of select="$listName"/>
										<xsl:text>Sort=a&amp;</xsl:text>
										<xsl:call-template name="replace-string">
											<xsl:with-param name="text" select="$unparsedQuery"/>
											<xsl:with-param name="from"><xsl:value-of
												select="$listName"/>Sort=n</xsl:with-param>
											<xsl:with-param name="to"/>
										</xsl:call-template>
									</xsl:attribute>
									<xsl:choose>
										<xsl:when test="contains($listName, 'year')">
											<xsl:element name="img">
												<xsl:attribute name="src">
												<xsl:value-of select="$sort_year"/>
												</xsl:attribute>
												<xsl:attribute name="alt">Sort by
												year</xsl:attribute>
											</xsl:element>
										</xsl:when>
										<xsl:otherwise>
											<xsl:element name="img">
												<xsl:attribute name="src">
												<xsl:value-of select="$sort_AZ"/>
												</xsl:attribute>
												<xsl:attribute name="alt">Sort
												alphabetically</xsl:attribute>
											</xsl:element>
										</xsl:otherwise>
									</xsl:choose>
								</xsl:element>
							</xsl:element>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:element name="li">
						<xsl:element name="a">
							<xsl:attribute name="href">
								<xsl:text>results?</xsl:text>
								<xsl:value-of select="$listName"/>
								<xsl:text>More=0&amp;</xsl:text>
								<xsl:call-template name="replace-string">
									<xsl:with-param name="text" select="$unparsedQuery"/>
									<xsl:with-param name="from"><xsl:value-of select="$listName"
										/>More=1</xsl:with-param>
									<xsl:with-param name="to"/>
								</xsl:call-template>
							</xsl:attribute>
							<xsl:element name="img">
								<xsl:attribute name="src">
									<xsl:value-of select="$HS_hide"/>
								</xsl:attribute>
								<xsl:attribute name="alt">Hide</xsl:attribute>
							</xsl:element>
						</xsl:element>
					</xsl:element>
				</div>
				<div class="facetpanelcontent">
					<!-- start at first of branch -->
					<xsl:choose>
						<xsl:when test="($listSort = 'a') and contains($listName,'year')">
							<xsl:for-each select="./int">
								<xsl:sort select="@name" order="descending"/>
								<xsl:if test="normalize-space(./@name)">
									<xsl:element name="li">
										<xsl:element name="a">
											<xsl:attribute name="href"
												><xsl:text>results?</xsl:text><xsl:value-of
												select="$listName"
												/><xsl:text>=</xsl:text><xsl:value-of
												select="./@name"/>&amp;<xsl:value-of
												select="$unparsedQuery"/>
											</xsl:attribute>
											<xsl:value-of select="./@name"/>&#160;(<xsl:value-of
												select="."/>) </xsl:element>
									</xsl:element>
								</xsl:if>
							</xsl:for-each>
						</xsl:when>
						<xsl:when test="$listSort = 'a'">
							<xsl:for-each select="./int">
								<xsl:sort select="@name"/>
								<xsl:if test="normalize-space(./@name)">
									<xsl:element name="li">
										<xsl:element name="a">
											<xsl:attribute name="href"
												><xsl:text>results?</xsl:text><xsl:value-of
												select="$listName"
												/><xsl:text>=</xsl:text><xsl:value-of
												select="./@name"/>&amp;<xsl:value-of
												select="$unparsedQuery"/>
											</xsl:attribute>
											<xsl:value-of select="./@name"/>&#160;(<xsl:value-of
												select="."/>) </xsl:element>
									</xsl:element>
								</xsl:if>
							</xsl:for-each>
						</xsl:when>
						<xsl:otherwise>
							<xsl:for-each select="./int">
								<xsl:if test="normalize-space(./@name)">
									<xsl:element name="li">
										<xsl:element name="a">
											<xsl:attribute name="href"
												><xsl:text>results?</xsl:text><xsl:value-of
												select="$listName"
												/><xsl:text>=</xsl:text><xsl:value-of
												select="./@name"/>&amp;<xsl:value-of
												select="$unparsedQuery"/>
											</xsl:attribute>
											<xsl:value-of select="./@name"/>&#160;(<xsl:value-of
												select="."/>) </xsl:element>
									</xsl:element>
								</xsl:if>
							</xsl:for-each>
						</xsl:otherwise>
					</xsl:choose>
				</div>
				<xsl:choose>
					<xsl:when test="$listSort = 'a'">
						<xsl:element name="li">
							<xsl:element name="a">
								<xsl:attribute name="href">
									<xsl:text>results?</xsl:text>
									<xsl:value-of select="$listName"/>
									<xsl:text>Sort=n&amp;</xsl:text>
									<xsl:call-template name="replace-string">
										<xsl:with-param name="text" select="$unparsedQuery"/>
										<xsl:with-param name="from"><xsl:value-of select="$listName"
											/>Sort=a</xsl:with-param>
										<xsl:with-param name="to"/>
									</xsl:call-template>
								</xsl:attribute>
								<xsl:element name="img">
									<xsl:attribute name="src">
										<xsl:value-of select="$sort_hits"/>
									</xsl:attribute>
									<xsl:attribute name="alt">Sort by Hit count</xsl:attribute>
								</xsl:element>
							</xsl:element>
						</xsl:element>
					</xsl:when>
					<xsl:otherwise>
						<xsl:element name="li">
							<xsl:element name="a">
								<xsl:attribute name="href">
									<xsl:text>results?</xsl:text>
									<xsl:value-of select="$listName"/>
									<xsl:text>Sort=a&amp;</xsl:text>
									<xsl:call-template name="replace-string">
										<xsl:with-param name="text" select="$unparsedQuery"/>
										<xsl:with-param name="from"><xsl:value-of select="$listName"
											/>Sort=n</xsl:with-param>
										<xsl:with-param name="to"/>
									</xsl:call-template>
								</xsl:attribute>
								<xsl:element name="img">
									<xsl:attribute name="src">
										<xsl:value-of select="$sort_AZ"/>
									</xsl:attribute>
									<xsl:attribute name="alt">Sort alphabetically</xsl:attribute>
								</xsl:element>
							</xsl:element>
						</xsl:element>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
			<xsl:element name="li">
				<xsl:element name="a">
					<xsl:attribute name="href">
						<xsl:text>results?</xsl:text>
						<xsl:value-of select="$listName"/>
						<xsl:text>More=0&amp;</xsl:text>
						<xsl:call-template name="replace-string">
							<xsl:with-param name="text" select="$unparsedQuery"/>
							<xsl:with-param name="from"><xsl:value-of select="$listName"
								/>More=1</xsl:with-param>
							<xsl:with-param name="to"/>
						</xsl:call-template>
					</xsl:attribute>
					<xsl:element name="img">
						<xsl:attribute name="src">
							<xsl:value-of select="$HS_hide"/>
						</xsl:attribute>
						<xsl:attribute name="alt">Hide</xsl:attribute>
					</xsl:element>
				</xsl:element>
			</xsl:element>
		</ul>
	</xsl:template>

	<xsl:template name="ListBrief">
		<xsl:param name="listName"/>
		<xsl:param name="listSolr"/>
		<ul class="options">
			<xsl:for-each
				select="//response/lst[@name='facet_counts']/lst[@name='facet_fields']/lst[@name=$listSolr]">
				<!-- start at first of branch -->
				<xsl:choose>
					<xsl:when test="contains($listName, 'year')">
						<xsl:for-each select="./int">
							<xsl:sort select="@name" order="descending"/>
							<xsl:if test="position() &lt; 7">
								<xsl:element name="li">
									<xsl:element name="a">
										<xsl:attribute name="href"
												><xsl:text>results?</xsl:text><xsl:value-of
												select="$listName"/><xsl:text>=</xsl:text>
											<xsl:call-template name="replace-string">
												<xsl:with-param name="text" select="./@name"/>
												<xsl:with-param name="from">&amp;</xsl:with-param>
												<xsl:with-param name="to">%26</xsl:with-param>
											</xsl:call-template>&amp;<xsl:value-of
												select="$unparsedQuery"/>
										</xsl:attribute>
										<xsl:value-of select="./@name"/>&#160;(<xsl:value-of
											select="."/>) </xsl:element>
								</xsl:element>
							</xsl:if>
						</xsl:for-each>
					</xsl:when>
					<xsl:otherwise>
						<xsl:for-each select="./int">
							<xsl:if test="normalize-space(./@name)">
								<xsl:if test="position() &lt; 7">
									<xsl:element name="li">
										<xsl:element name="a">
											<xsl:attribute name="href"
												><xsl:text>results?</xsl:text><xsl:value-of
												select="$listName"
												/><xsl:text>=</xsl:text><xsl:call-template
												name="replace-string">
												<xsl:with-param name="text" select="./@name"/>
												<xsl:with-param name="from">&amp;</xsl:with-param>
												<xsl:with-param name="to">%26</xsl:with-param>
												</xsl:call-template>&amp;<xsl:value-of
												select="$unparsedQuery"/>
											</xsl:attribute>
											<xsl:value-of select="./@name"/>&#160;(<xsl:value-of
												select="."/>) </xsl:element>
									</xsl:element>
								</xsl:if>
							</xsl:if>
						</xsl:for-each>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
			<xsl:element name="li">
				<xsl:element name="a">
					<xsl:attribute name="href">
						<xsl:text>results?</xsl:text>
						<xsl:value-of select="$listName"/>
						<xsl:text>More=1&amp;</xsl:text>
						<xsl:call-template name="replace-string">
							<xsl:with-param name="text" select="$unparsedQuery"/>
							<xsl:with-param name="from"><xsl:value-of select="$listName"
								/>More=0</xsl:with-param>
							<xsl:with-param name="to"/>
						</xsl:call-template>
						<xsl:if test="contains($listName, 'year')">&amp;yearSort=a</xsl:if>
					</xsl:attribute>
					<xsl:element name="img">
						<xsl:attribute name="src">
							<xsl:value-of select="$HS_see"/>
						</xsl:attribute>
						<xsl:attribute name="alt">See the rest</xsl:attribute>
					</xsl:element>
				</xsl:element>
			</xsl:element>
		</ul>
	</xsl:template>

	<xsl:template name="ListShort">
		<xsl:param name="listName"/>
		<xsl:param name="listSolr"/>
		<ul class="options">
			<xsl:for-each
				select="//response/lst[@name='facet_counts']/lst[@name='facet_fields']/lst[@name=$listSolr]">
				<!-- start at first of branch -->
				<xsl:for-each select="./int">
					<xsl:if test="normalize-space(./@name)">
						<xsl:if test="position() &lt; 7">
							<xsl:element name="li">
								<xsl:element name="a">
									<xsl:attribute name="href"
											><xsl:text>results?</xsl:text><xsl:value-of
											select="$listName"/><xsl:text>=</xsl:text>
										<xsl:call-template name="replace-string">
											<xsl:with-param name="text" select="./@name"/>
											<xsl:with-param name="from">&amp;</xsl:with-param>
											<xsl:with-param name="to">%26</xsl:with-param>
										</xsl:call-template>&amp;<xsl:value-of
											select="$unparsedQuery"/>
									</xsl:attribute>
									<xsl:value-of select="./@name"/>&#160;(<xsl:value-of select="."
									/>) </xsl:element>
							</xsl:element>
						</xsl:if>
					</xsl:if>
				</xsl:for-each>
			</xsl:for-each>
		</ul>
	</xsl:template>


	<!--  Utility templates  -->
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

	<xsl:template name="replace-string">
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
	</xsl:template>

</xsl:stylesheet>
