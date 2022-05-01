import discord

from discord_components import DiscordComponents, Button, ButtonStyle
from discord.ext import commands

token = open("TOKEN.txt", "r").readline()

description = "Hi, I'm Millie! I help artists combat art theft."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

embed_color = 0xe6c9ff

@bot.event
async def on_ready():
    DiscordComponents(bot) # Supports functional buttons
    print("Millie is ready for action!")

@bot.command()
async def info(ctx):
    """Provides the author with info about Millie."""
    info = discord.Embed(
        title="Hi, I'm Millie! I'm here to help artists combat art theft.",
        description="""
        As a digital artist, it can be incredibly frustrating when someone steals your work and tries to profit off of it.
        Thankfully, there's a law called the Digital Millenium Copyright Act (DMCA) that can help you get your stolen content removed.
        Many websites have __online forms__ for submitting your DMCA takedown notice.
        If such a form doesn't exist, you can __contact the site's DMCA agent directly__ or __reach out to the web host or ISP__.

        Type **!email** to learn more about DMCA takedown emails.
        Type **!forms** for help with DMCA forms for a particular site.
        """,
        color=embed_color
        )
    await ctx.send(embed=info)

@bot.command()
async def email(ctx):

    #Introduction

    intro = discord.Embed(
        title="Sending a DMCA email to a service provider is one way of getting your stolen content removed from their site.",
        description="""
        I'll ask you a few questions about the incident you'd like to report.
        Then I'll generate an email that you can send to a service provider.

        Is that okay? Click **Next** to proceed.
        """,
        color=embed_color
    )
    intro_next_btn = Button(style=ButtonStyle.blue, label="Next", custom_id="intro_next_btn")
    await ctx.send(embed=intro, components=[intro_next_btn])
    
    intro_interaction = await bot.wait_for(
        "button_click", check=lambda btn: btn.custom_id == "intro_next_btn"
    )

    await intro_interaction.send(content="Let's begin!")
    
    #Step 1: Describe your content

    step_1 = discord.Embed(
        title="Step 1: Describe your content",
        description="""
        Provide a description of the content that is being infringed upon.

        *__Example:__ a digital painting of a young lady sitting down at a table, wearing a lavender shirt and headphones, with her laptop open in front of her...*
        """,
        color=embed_color
    )    

    await ctx.send(embed=step_1)

    step_1_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Step 2: Original links

    step_2 = discord.Embed(
        title="Step 2: Original links to your content",
        description="""
        Please provide the link(s) where *you*, the creator, originally posted your content.
        """,
        color=embed_color
    )   

    await ctx.send(embed=step_2)   

    step_2_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Step 3: Location of the infringing content

    step_3 = discord.Embed(
        title="Step 3: Location of the infringing content",
        description="""
        Please provide the link(s) where *the infringing (stolen) copy of the content* is located.
        """,
        color=embed_color
    )   

    await ctx.send(embed=step_3)   

    step_3_interaction = await bot.wait_for(
        "message", check=lambda msg: msg.author == ctx.author
    )

    # Final step: Generate your email

    final_step = discord.Embed(
        title="Thank you!",
        description="""
        Click the button below to generate your DMCA takedown email.

        Before you send the email to a DMCA agent, replace the fields in bold with your personal contact information.

        Use your **full legal name**, as the DMCA takedown notice is a legal action.
        """,
        color=embed_color        
    )
    email_btn = Button(style=ButtonStyle.green, label="📧 Generate DMCA Email", custom_id="email_btn")

    await ctx.send(embed=final_step,components=[email_btn])

    final_step_interaction = await bot.wait_for(
        "button_click", check=lambda i: i.custom_id == "email_btn"
    )

    content_description = step_1_interaction.content
    original_links = step_2_interaction.content
    infringing_links = step_3_interaction.content

    dmca_email = discord.Embed(
    title="Subject: Notice of Copyright Violation (DMCA Takedown Notice) - Request to Remove Offending Content",
    description=f"""
    
    To whom it may concern:
    
    My name is **[Replace with your full legal name]**. The following information is presented for the purposes of removing web content that infringes on my copyright per the Digital Millennium Copyright Act (“DMCA”). This notice constitutes an official notification under Section 512(c) of the DMCA.

    Under that statute, you are required, as a service provider, to remove or disable access to the infringing materials specified below upon receipt of this notice. Under the safe harbor provision of the DMCA, you are given immunity from liability for hosting the infringing content, provided that you quickly rectify and investigate the copyright infringement. Failure to do so can result in the loss of this statutory immunity.

    The content that is being infringed is {content_description}.

    The original content is located at the following URL(s):
    [{original_links}]({original_links})

    The infringing copy of this content is located at the following URL(s):
    [{infringing_links}]({infringing_links})

    I have a good faith belief that the use of the copyrighted materials described above on the allegedly infringing web pages is not authorized by the copyright owner, its agent or the law. Under penalty of perjury I certify that the information contained in this notification is both true and accurate, and that I am the owner of the copyrights involved.

    For further inquiry, I may be contacted as follows:
    **[Replace with your own email address or phone number]**

    Sincerely,
    **[Replace with your full legal name]**
        
    
    """,
    color=embed_color
    )

    await final_step_interaction.send(embed=dmca_email)

bot.run(token)