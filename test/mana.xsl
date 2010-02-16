<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<xsl:import href="f1/trignm.xsl"/>
<xsl:import href="f1/sqrt.xsl"/>

<xsl:template match="/test">
	<xsl:call-template name="building">
		<xsl:with-param name="limit0" select="0"/>
		<xsl:with-param name="limit1" select="$pi div 3"/>
	</xsl:call-template>
</xsl:template>

<xsl:template match="/board">
	<html>
		<head>
			<link type="text/css" rel="stylesheet" href="mana.css" />
		</head>
		<body>
			<div style="position: absolute; top: 100px; left: 200px;">
				<xsl:apply-templates />
			</div>
		</body>
	</html>
</xsl:template>

<xsl:template match="building" name="building">
	<xsl:param name="limit0" select="0"/>
	<xsl:param name="limit1" select="$pi"/>

	<xsl:variable name="_tmp1">
		<xsl:call-template name="cos">
			<xsl:with-param name="pX" select="$limit1 - $limit0"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="_tmp2">
		<xsl:call-template name="sqrt">
			<xsl:with-param name="N" select="2 - (2 * $_tmp1)"/>
			<xsl:with-param name="Eps" select="0.01"/>
		</xsl:call-template>
	</xsl:variable>

	<!-- depth component of polar coordinate !-->
	<xsl:variable name="depth" select="2.0 div $_tmp2"/>

	<xsl:variable name="x">
		<xsl:call-template name="cos">
			<xsl:with-param name="pX" select="$limit0 + (($limit1 - $limit0) div 2)"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="y">
		<xsl:call-template name="sin">
			<xsl:with-param name="pX" select="$limit0 + (($limit1 - $limit0) div 2)"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="step" select="($limit1 - $limit0) div count(building)"/>

	<div class="building">
		<xsl:attribute name="style">position: absolute; top: <xsl:value-of select="$y * $depth * 32"/>px; left: <xsl:value-of select="$x * $depth * 32"/>px;
		</xsl:attribute>
		<b><xsl:value-of select="@type"/></b>
	</div>

	<xsl:for-each select="building" >
		<xsl:apply-templates select=".">
			<xsl:with-param name="limit0" select="$limit0 + (position() - 1) * $step"/>
			<xsl:with-param name="limit1" select="$limit0 + position() * $step"/>
		</xsl:apply-templates>

<!--
		<span class="limit0"><xsl:value-of select="$limit0 + (position() -1) * $step"/></span>
		<span class="limit1"><xsl:value-of select="$limit0 + position() * $step"/></span>
!-->
	</xsl:for-each>
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
