<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<xsl:template match="/board">
	<html>
		<head>
			<link type="text/css" rel="stylesheet" href="mana.css" />
		</head>
		<body>
			<div>
				<h1>BOARD</h1>
				<xsl:apply-templates />
			</div>
		</body>
	</html>
</xsl:template>

<xsl:template match="boardSection">
	<div class="boardsection">
		<b><xsl:value-of select="@player" />'s section</b>
		<xsl:apply-templates />
	</div>
</xsl:template>

<xsl:template match="building">
	<div class="building">
		<div>
			<xsl:attribute name="class"><xsl:value-of select="@type"/></xsl:attribute>
			<b><xsl:value-of select="@type"/></b>
			<div class="units">
				<xsl:apply-templates select="creature"/>
			</div>
		</div>
		<div class="children">
			<xsl:apply-templates select="building" />
		</div>
	</div>
</xsl:template>

<xsl:template match="creature">
	<div class="creature">
		<div>
			<xsl:attribute name="class"><xsl:value-of select="@type"/></xsl:attribute>
			<span>
				<xsl:attribute name="class"><xsl:value-of select="@alignment"/></xsl:attribute>
				<xsl:value-of select="@type"/>
			</span>
		</div>
	</div>
</xsl:template>

</xsl:stylesheet>
